# 🎵 Ultimate Music Migrator  
### Spotify ↔ Tidal | High-Precision Playlist & Library Transfer

A robust, bi-directional Python tool designed to migrate playlists and **Liked Tracks** between **Spotify** and **Tidal** with maximum accuracy and data integrity.

---

## 🚀 Overview

Ultimate Music Migrator focuses on **precision over speed**, ensuring that tracks are matched correctly even across different catalog versions, remasters, or releases.  
It includes a dedicated **integrity auditing system** to verify that migrations are truly complete.

---

## ✨ Key Features

- 🔁 **Bi-Directional Migration**  
  Seamlessly transfer music from **Spotify → Tidal** or **Tidal → Spotify**.

- 🎯 **Sniper Matching Engine**  
  Uses **ISRC codes** combined with **heuristic duration matching (±3 seconds)** to avoid incorrect remixes, live versions, or alternate takes.

- 🧪 **Integrity Auditor (`espejo.py`)**  
  A specialized verification tool that:
  - Confirms 100% track presence
  - Detects missing or mismatched songs
  - Works regardless of playlist order

- 🧠 **Smart Ordering System**  
  - Preserve original *Date Added* order  
  - Or reverse playlists chronologically

- 🌍 **Order-Independent Matching**  
  The auditor identifies matches even if playlists are sorted differently between platforms.

---

## 🛠️ Requirements

- Python **3.x**
- Spotify Developer Account  
  - Client ID  
  - Client Secret
- Tidal Account

---

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Saturnoook/Music-Migrator-TIDAL-and-Spotify.git
cd Music-Migrator-TIDAL-and-Spotify
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Credentials
1. Locate `my_data_example.txt`
2. Rename it to `my_data.py`
3. Open the file and insert your API credentials
4. Save the file

## 🔐 Credentials & `my_data.py` Setup (Step-by-Step)

This project requires credentials for **Spotify** and **TIDAL**.

> ✅ Tip: Keep your secrets out of Git. Add `my_data.py` to `.gitignore` and never commit it.

---

### 1) Create `my_data.py`

1. Find `my_data_example.txt`
2. Rename it to **`my_data.py`**
3. Fill in the values as explained below

---

## 🟢 Spotify Credentials (Client ID / Client Secret / Redirect URI)

### A) Create a Spotify Developer App
1. Open the Spotify Developer Dashboard:  
   https://developer.spotify.com/dashboard
2. Click **Create app** (or similar).
3. After creating the app, open its **Settings** to view:
   - **Client ID**
   - **Client Secret**

Helpful docs:
- Apps (Client ID / Secret): https://developer.spotify.com/documentation/web-api/concepts/apps
- Getting started (where to find credentials): https://developer.spotify.com/documentation/web-api/tutorials/getting-started

---

### B) Set the Redirect URI (VERY IMPORTANT)
Your Redirect URI in Spotify Dashboard must **exactly match** the one in `my_data.py`.

This project uses:
- `http://localhost:8888/callback`

⚠️ Spotify may require loopback IP instead of `localhost` in some cases:
- `http://127.0.0.1:8888/callback`

Steps:
1. In your Spotify app settings, find **Redirect URIs**
2. Add one of these:
   - `http://localhost:8888/callback`
   - `http://127.0.0.1:8888/callback`
3. Save changes.

Docs:
- Redirect URIs concept: https://developer.spotify.com/documentation/web-api/concepts/redirect_uri  
- Spotify note about migrating away from insecure redirect URIs:  
  https://developer.spotify.com/documentation/web-api/tutorials/migration-insecure-redirect-uri

✅ If you change the redirect URI in the dashboard, update `SPOTIPY_REDIRECT_URI` in `my_data.py` too.

---

## 🔵 TIDAL Credentials (Email / Password / Numeric User ID)

### A) Username + Password
Use your normal TIDAL login:
- `tidal_username` = your TIDAL email
- `tidal_pwd` = your TIDAL password

---

### B) Get your TIDAL Numeric User ID (`tidal_id`)

#### Option 1 (Recommended): Print it with a Python one-liner
This avoids browser DevTools entirely.

```bash
python -c "import tidalapi; s=tidalapi.Session(); s.login('YOUR_TIDAL_EMAIL','YOUR_TIDAL_PASSWORD'); print(s.user.id)"
```

Copy the printed number into:
```py
tidal_id = "PASTE_THE_NUMBER_HERE"
```

#### Option 2: Use the Browser Network Tab (Advanced)
1. Open TIDAL Web Player and log in.
2. Open DevTools → **Network**.
3. Navigate to your profile/account area.
4. Filter requests by `users` (or look for a request containing `/users/`).
5. You’ll typically see a request like:
   - `/users/<YOUR_NUMERIC_ID>` or similar  
6. Copy that numeric ID into `tidal_id`.

Reference (API-style endpoints):  
https://tidal-music.github.io/tidal-api-reference/

---

## ✅ Security (Recommended)

### Add to `.gitignore`
Make sure you ignore your secrets:

```gitignore
# Credentials (DO NOT COMMIT)
my_data.py
.env
```

---

## 🧪 Quick Sanity Check
After filling `my_data.py`, run:

```bash
python script.py
```

Then verify integrity with:

```bash
python espejo.py
```



> ⚠️ **Important:** Never commit `my_data.py` to a public repository.

---

## 🚀 Usage

### Run the Migration Tool
```bash
python script.py
```

### Run the Integrity Auditor
```bash
python espejo.py
```

The auditor will validate that every track was transferred correctly, even if playlist ordering differs.

---

## 🧩 Project Structure (Simplified)

```text
├── script.py        # Main migration engine
├── espejo.py        # Integrity & verification tool
├── my_data.py       # API credentials (ignored by git)
├── requirements.txt # Python dependencies
└── README.md
```

---

## 📄 Credits & Dependencies

This project is built on top of the following libraries:

- `spotipy` – Spotify Web API client
- `tidalapi` – Tidal API interface

---

## ⚖️ Disclaimer

This project is intended for **personal use** only.  
Users are responsible for complying with Spotify and Tidal terms of service.

---

## ⭐ Support the Project

If this tool helped you:
- Star ⭐ the repository
- Share feedback or open an issue
- Contribute improvements or fixes

