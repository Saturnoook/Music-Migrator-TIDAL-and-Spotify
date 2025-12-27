🎵 Ultimate Music Migrator (Spotify ↔ Tidal)

A high-precision Python tool to migrate playlists and "Liked Tracks" between Spotify and Tidal bi-directionally.

✨ Features
* **Bi-Directional:** Move music from Tidal to Spotify OR Spotify to Tidal.
* **Sniper Mode:** Uses ISRC codes and heuristic duration matching (±3s) to prevent incorrect remixes.
* **Integrity Auditor:** Includes a specialized script (`espejo.py`) to verify 100% data transfer integrity.
* **Smart Ordering:** Preserve "Date Added" order or reverse it chronologically.
* **Global Match:** The auditor detects matches regardless of the sort order.

🛠️ Requirements
* Python 3.x
* Spotify Developer Account (Client ID / Secret)
* Tidal Account

📦 Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install spotipy tidalapi