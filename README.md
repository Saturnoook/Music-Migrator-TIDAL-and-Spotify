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
