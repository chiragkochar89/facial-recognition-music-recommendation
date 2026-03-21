"""
Generate emotion-based CSVs for specific languages (Hindi/Marathi) using Spotify playlists.

- Reads a config mapping: emotion -> playlist IDs per language
- Fetches tracks and writes CSVs into songs/<emotion>_<lang>.csv

Requirements:
- pip install spotipy pandas
- Set environment variables SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET

Run:
  python scripts/generate_language_csvs.py --language hindi
  python scripts/generate_language_csvs.py --language marathi
"""
from __future__ import annotations
import os
import json
import time
import argparse
from typing import List, Dict
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SONGS_DIR = os.path.join(REPO_ROOT, "songs")
CONFIG_PATH = os.path.join(REPO_ROOT, "scripts", "language_playlists.json")

EMOTION_FILE_MAP = {
    "angry": "angry.csv",
    "disgusted": "disgusted.csv",
    "fearful": "fearful.csv",
    "happy": "happy.csv",
    "neutral": "neutral.csv",
    "sad": "sad.csv",
    "surprised": "surprised.csv",
}


def load_config() -> Dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_spotify_client() -> spotipy.Spotify:
    cid = os.getenv("SPOTIPY_CLIENT_ID")
    secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    if not cid or not secret:
        raise RuntimeError("Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET env vars.")
    auth_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    return spotipy.Spotify(auth_manager=auth_manager)


def playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> List[Dict]:
    results = sp.playlist_items(playlist_id, additional_types=["track"], limit=100)
    items = results.get("items", [])
    while results.get("next"):
        results = sp.next(results)
        items.extend(results.get("items", []))
    tracks = []
    for it in items:
        t = it.get("track") or {}
        if not t:
            continue
        tracks.append({
            "Name": t.get("name"),
            "Album": (t.get("album") or {}).get("name"),
            "Artist": ", ".join([a.get("name") for a in (t.get("artists") or []) if a and a.get("name")]),
            "URL": (t.get("external_urls") or {}).get("spotify"),
        })
    return tracks


def write_csv_for_emotion(language: str, emotion: str, playlist_id: str, sp: spotipy.Spotify) -> str:
    tracks = playlist_tracks(sp, playlist_id)
    if not tracks:
        raise RuntimeError(f"No tracks pulled for {language}/{emotion} from {playlist_id}")
    df = pd.DataFrame(tracks, columns=["Name", "Album", "Artist", "URL"])  # consistent with app expectations
    df["Language"] = language  # add Language column for filtering in app
    out_name = os.path.splitext(EMOTION_FILE_MAP[emotion])[0] + f"_{language}.csv"
    out_path = os.path.join(SONGS_DIR, out_name)
    df.to_csv(out_path, index=False, encoding="utf-8")
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", required=True, choices=["hindi", "marathi"], help="Language to generate CSVs for")
    args = parser.parse_args()

    cfg = load_config()
    lang_cfg = cfg.get(args.language)
    if not lang_cfg:
        raise SystemExit(f"No config for language: {args.language}")

    os.makedirs(SONGS_DIR, exist_ok=True)
    sp = get_spotify_client()

    generated = []
    for emotion, playlist_id in lang_cfg.items():
        if emotion not in EMOTION_FILE_MAP:
            print(f"Skipping unknown emotion key: {emotion}")
            continue
        try:
            print(f"Generating {emotion} for {args.language} from {playlist_id}...")
            path = write_csv_for_emotion(args.language, emotion, playlist_id, sp)
            generated.append(path)
            time.sleep(0.2)
        except Exception as e:
            print(f"Failed {emotion}/{args.language}: {e}")

    print("Done. Generated:")
    for p in generated:
        print(" -", p)


if __name__ == "__main__":
    main()