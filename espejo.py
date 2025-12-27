from my_data import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tidalapi.session import Session
import re
import unicodedata

# ==========================================
# NORMALIZATION UTILS
# ==========================================
def normalize_text(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\[[^]]*\]', '', text)
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def create_fingerprint(title, artist):
    return f"{normalize_text(title)}|{normalize_text(artist)}"

# ==========================================
# DATA FETCHING
# ==========================================
def get_all_tidal_tracks(session):
    print("\n🌊 LOADING TIDAL DATA...")
    print("[1] Specific Playlist")
    print("[2] All My Likes")
    opt = input("Option: ")
    tracks = []
    
    if opt == '1':
        pls = list(session.user.playlists())
        for i, pl in enumerate(pls):
            print(f"[{i}] {pl.name}")
        try:
            sel = int(input("Select: "))
            print("📥 Downloading list...")
            for t in pls[sel].tracks():
                if t: tracks.append({'title': t.name, 'artist': t.artist.name, 'obj': t})
        except: pass
        
    elif opt == '2':
        print("📥 Downloading ALL Likes (Paged)...")
        user_id = session.user.id
        offset = 0
        while True:
            try:
                params = {'limit': 50, 'offset': offset, 'order': 'DATE', 'orderDirection': 'DESC'}
                req = session.request.request('GET', f'users/{user_id}/favorites/tracks', params=params)
                items = req.json().get('items', [])
                if not items: break
                for item in items:
                    t = item.get('item')
                    if t: tracks.append({'title': t.get('title'), 'artist': t.get('artist', {}).get('name'), 'obj': t})
                print(f"   -> {len(tracks)} tracks read...")
                offset += 50
            except: break
            
    return tracks

def get_all_spotify_tracks(sp):
    print("\n🟢 LOADING SPOTIFY DATA...")
    print("[1] Specific Playlist")
    print("[2] All My Likes")
    opt = input("Option: ")
    tracks = []

    if opt == '1':
        results = sp.current_user_playlists()
        items = results['items']
        while results['next']:
            items.extend(sp.next(results)['items'])
        
        for i, pl in enumerate(items):
            print(f"[{i}] {pl['name']}")
        try:
            sel = int(input("Select: "))
            pl_id = items[sel]['id']
            print("📥 Downloading list...")
            res = sp.playlist_items(pl_id)
            items_pl = res['items']
            while res['next']:
                res = sp.next(res)
                items_pl.extend(res['items'])
            for item in items_pl:
                t = item.get('track')
                if t: tracks.append({'title': t['name'], 'artist': t['artists'][0]['name'], 'obj': t})
        except: pass

    elif opt == '2':
        print("📥 Downloading ALL Likes...")
        res = sp.current_user_saved_tracks(limit=50)
        items = res['items']
        while res['next']:
            print(f"   -> {len(tracks) + len(items)} tracks read...")
            res = sp.next(res)
            items.extend(res['items'])
        
        for item in items:
            t = item.get('track')
            if t: tracks.append({'title': t['name'], 'artist': t['artists'][0]['name'], 'obj': t})
            
    return tracks

# ==========================================
# AUDIT ENGINE
# ==========================================
def audit_lists(tidal_list, spotify_list):
    print("\n" + "="*60)
    print("      STARTING CROSS-PLATFORM AUDIT      ")
    print("="*60)
    print(f"Total Tidal:   {len(tidal_list)}")
    print(f"Total Spotify: {len(spotify_list)}")
    print("Analyzing matches (Order Independent)...")

    spotify_map = {}
    for t in spotify_list:
        fp = create_fingerprint(t['title'], t['artist'])
        spotify_map[fp] = t

    missing_in_spotify = []
    found_count = 0

    for t in tidal_list:
        fp = create_fingerprint(t['title'], t['artist'])
        if fp in spotify_map:
            found_count += 1
        else:
            missing_in_spotify.append(t)

    print("\n" + "="*60)
    print("             AUDIT RESULTS             ")
    print("="*60)
    
    success_rate = (found_count / len(tidal_list)) * 100 if tidal_list else 0
    
    print(f"✅ FOUND MATCHES: {found_count}")
    print(f"❌ MISSING:       {len(missing_in_spotify)}")
    print(f"📊 INTEGRITY:     {success_rate:.2f}%")
    
    if missing_in_spotify:
        print("\n⚠️  TRACKS NOT TRANSFERRED:")
        print("-" * 50)
        for i, t in enumerate(missing_in_spotify):
            print(f"{i+1}. {t['title']} - {t['artist']}")
        print("-" * 50)
    else:
        print("\n✨ PERFECT! 100% Data Integrity confirmed.")

# ==========================================
# MAIN
# ==========================================
def main():
    try:
        session = Session()
        try: session.login(tidal_username, tidal_pwd)
        except: session.login_oauth_simple()

        auth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI, scope="user-library-read playlist-read-private")
        sp = spotipy.Spotify(auth_manager=auth)

        t_tracks = get_all_tidal_tracks(session)
        if not t_tracks: return

        s_tracks = get_all_spotify_tracks(sp)
        if not s_tracks: return

        audit_lists(t_tracks, s_tracks)

    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPress ENTER to exit...")

if __name__ == '__main__':
    main()