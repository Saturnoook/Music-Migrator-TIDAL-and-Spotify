# --- IMPORTS CORREGIDOS ---
from my_data import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tidalapi
from tidalapi.session import Session
import re

# --- CONFIGURATION ---
DURATION_TOLERANCE_SEC = 3

# ==========================================
# UTILS
# ==========================================
def clean_title(title):
    if not title: return ""
    title = re.sub(r'\s*[\(\[].*?(remaster|live|mix|edit|version|feat|ft\.).*?[\)\]]', '', title, flags=re.IGNORECASE)
    return title.strip()

# ==========================================
# TIDAL TOOLS
# ==========================================
def login_tidal():
    print(f"🌊 Connecting to Tidal ({tidal_username})...")
    session = Session()
    try:
        session.login(tidal_username, tidal_pwd)
        if session.check_login():
            print("✅ Tidal: Connected (Native).")
            return session
    except:
        pass
    print("⚠️ Native login failed. Using Web Auth...")
    session.login_oauth_simple()
    print("✅ Tidal: Connected (Web).")
    return session

def get_tidal_tracks_source(session):
    print("\n--- SOURCE: TIDAL ---")
    print("[1] Specific Playlist")
    print("[2] My Liked Tracks (Favorites)")
    opt = input("Choose option: ")

    tracks_data = [] 
    source_name = ""

    if opt == '1':
        playlists = session.user.playlists()
        local_pls = list(playlists)
        if not local_pls:
            print("❌ No playlists found in Tidal.")
            return [], ""

        for i, pl in enumerate(local_pls):
            print(f"[{i}] {pl.name}")
        
        try:
            sel = int(input("Select playlist number: "))
            target_pl = local_pls[sel]
            source_name = f"{target_pl.name} (Tidal)"
            print(f"📥 Downloading tracks from '{target_pl.name}'...")
            for t in target_pl.tracks():
                if t: tracks_data.append({
                    'name': t.name,
                    'artist': t.artist.name,
                    'album': t.album.name,
                    'duration': t.duration,
                    'isrc': getattr(t, 'isrc', None)
                })
        except:
            print("❌ Invalid selection.")
            return [], ""

    elif opt == '2':
        print("\n📥 Extracting Likes (Order: DATE ADDED)...")
        user_id = session.user.id
        limit = 50
        offset = 0
        while True:
            params = {'limit': limit, 'offset': offset, 'order': 'DATE', 'orderDirection': 'DESC'}
            try:
                req = session.request.request('GET', f'users/{user_id}/favorites/tracks', params=params)
                data = req.json()
                items = data.get('items', [])
                if not items: break
                
                for item in items:
                    track_info = item.get('item')
                    if track_info:
                        tracks_data.append({
                            'name': track_info.get('title'),
                            'artist': track_info.get('artist', {}).get('name'),
                            'album': track_info.get('album', {}).get('title'),
                            'duration': track_info.get('duration', 0),
                            'isrc': track_info.get('isrc')
                        })
                print(f"   -> {len(tracks_data)} tracks loaded...")
                offset += limit
            except:
                break
        source_name = "Tidal Favorites"

    return tracks_data, source_name

# ==========================================
# SPOTIFY TOOLS
# ==========================================
def login_spotify():
    print("🟢 Connecting to Spotify...")
    scope_list = "playlist-modify-public playlist-modify-private playlist-read-private user-library-read"
    auth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope_list)
    sp = spotipy.Spotify(auth_manager=auth)
    print(f"✅ Spotify: Connected as {sp.current_user()['id']}")
    return sp, sp.current_user()['id']

def get_spotify_tracks_source(sp):
    print("\n--- SOURCE: SPOTIFY ---")
    print("[1] Specific Playlist")
    print("[2] My Liked Tracks (Saved Tracks)")
    opt = input("Choose option: ")
    tracks_data = []
    source_name = ""

    if opt == '1':
        print("⏳ Reading playlists...")
        results = sp.current_user_playlists()
        items = results['items']
        while results['next']: 
            results = sp.next(results)
            items.extend(results['items'])
        
        if not items: return [], ""
        for i, pl in enumerate(items):
            print(f"[{i}] {pl['name']}")
        
        try:
            sel = int(input("\nSelect playlist number: "))
            target_pl = items[sel]
            source_name = f"{target_pl['name']} (Spotify)"
            
            print(f"📥 Downloading...")
            res_tracks = sp.playlist_items(target_pl['id'])
            tracks_items = res_tracks['items']
            while res_tracks['next']:
                res_tracks = sp.next(res_tracks)
                tracks_items.extend(res_tracks['items'])
            
            for item in tracks_items:
                track = item.get('track')
                if track:
                    tracks_data.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'duration': track['duration_ms'] / 1000,
                        'isrc': track.get('external_ids', {}).get('isrc')
                    })
        except: return [], ""

    elif opt == '2':
        print("📥 Downloading Likes...")
        results = sp.current_user_saved_tracks(limit=50)
        tracks_items = results['items']
        while results['next']:
            print(f"   -> Loading... ({len(tracks_items)} found)")
            results = sp.next(results)
            tracks_items.extend(results['items'])
        for item in tracks_items:
            track = item.get('track')
            if track:
                tracks_data.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration': track['duration_ms'] / 1000,
                    'isrc': track.get('external_ids', {}).get('isrc')
                })
        source_name = "Spotify Favorites"
    return tracks_data, source_name

# ==========================================
# MIGRATION ENGINES
# ==========================================
def migrate_to_spotify(sp, sp_user_id, tracks, playlist_name):
    print(f"\n🚀 Target: Spotify | Creating playlist '{playlist_name}'...")
    new_pl = sp.user_playlist_create(sp_user_id, playlist_name, public=False)
    uris = []
    found_count = 0
    missed = 0
    
    print("🔎 Starting high-precision search (ISRC + Heuristics)...")

    for t in tracks:
        match_uri = None
        method = "FAIL"

        if t.get('isrc'):
            try:
                res = sp.search(q=f"isrc:{t['isrc']}", limit=1, type='track')
                if res['tracks']['items']:
                    match_uri = res['tracks']['items'][0]['uri']
                    method = "ISRC 🎯"
            except: pass
        
        if not match_uri:
            clean_name = clean_title(t['name'])
            query = f"track:{clean_name} artist:{t['artist']}".replace("'", "")
            try:
                res = sp.search(q=query, limit=5, type='track')
                if res['tracks']['items']:
                    for item in res['tracks']['items']:
                        diff = abs(t['duration'] - (item['duration_ms'] / 1000))
                        if diff <= DURATION_TOLERANCE_SEC:
                            match_uri = item['uri']
                            method = "Smart Match 🧠"
                            break
            except: pass
        
        if match_uri:
            uris.append(match_uri)
            print(f"✔ [{method}] {t['name']}")
            found_count += 1
        else:
            print(f"❌ {t['name']} (ISRC: {t.get('isrc')})")
            missed += 1
            
        if len(uris) >= 100:
            sp.playlist_add_items(new_pl['id'], uris)
            uris = []
            
    if uris: sp.playlist_add_items(new_pl['id'], uris)
    return found_count, missed

def migrate_to_tidal(session, tracks, playlist_name):
    print(f"\n🚀 Target: Tidal | Creating playlist '{playlist_name}'...")
    new_pl = session.user.create_playlist(playlist_name, "Imported from Spotify")
    found_count = 0
    missed = 0
    
    print("🔎 Starting high-precision search...")

    for t in tracks:
        match_id = None
        method = "FAIL"
        
        clean_name = clean_title(t['name'])
        query = f"{t['artist']} {clean_name}"
        
        try:
            res = session.search(query, models=[tidalapi.media.Track], limit=10)
            res_tracks = res['tracks']
        except: res_tracks = []
        
        if res_tracks:
            if t.get('isrc'):
                for item in res_tracks:
                    if getattr(item, 'isrc', '') == t['isrc']:
                        match_id = item.id
                        method = "ISRC 🎯"
                        break
            
            if not match_id:
                for item in res_tracks:
                    diff = abs(t['duration'] - item.duration)
                    if diff <= DURATION_TOLERANCE_SEC:
                        match_id = item.id
                        method = "Smart Match 🧠"
                        break
        
        if match_id:
            try:
                new_pl.add([match_id])
                print(f"✔ [{method}] {t['name']}")
                found_count += 1
            except Exception as e:
                print(f"⚠️ Error API: {t['name']} - {e}")
        else:
            print(f"❌ {t['name']}")
            missed += 1
            
    return found_count, missed

# ==========================================
# MAIN MENU (LA PARTE QUE FALTABA)
# ==========================================
def main():
    try:
        print("=========================================")
        print("   THE SNIPER MIGRATION TOOL V6 (PRO)    ")
        print("       Precision Mode Enabled            ")
        print("=========================================")
        
        session = login_tidal()
        sp, sp_uid = login_spotify()
        
        print("\nSelect Direction:")
        print("[1] TIDAL   ---> SPOTIFY")
        print("[2] SPOTIFY ---> TIDAL")
        direction = input("Choice (1/2): ")
        
        source_tracks = []
        pl_name_base = ""
        
        if direction == '1':
            source_tracks, pl_name_base = get_tidal_tracks_source(session)
        elif direction == '2':
            source_tracks, pl_name_base = get_spotify_tracks_source(sp)
        else: return

        if not source_tracks: return

        print(f"\nFound {len(source_tracks)} tracks.")
        print("Sorting preference:")
        print("[1] Original (Date Added)")
        print("[2] Reversed (Chronological)")
        if input("Choice: ") == '2':
            source_tracks.reverse()

        final_pl_name = f"{pl_name_base} (PRO IMPORT)"
        
        if direction == '1':
            ok, fail = migrate_to_spotify(sp, sp_uid, source_tracks, final_pl_name)
        else:
            ok, fail = migrate_to_tidal(session, source_tracks, final_pl_name)

        print("\n" + "="*30)
        print(f"🎉 FINAL REPORT: {ok} Success / {fail} Failed")
        print("==============================")

    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
    
    input("\nPress ENTER to exit...")

if __name__ == '__main__':
    main()