"""
Enhanced Spotify CSV generator for Emotion-based playlists.

- Handles English, Hindi, Marathi playlists.
- Skips invalid playlists and continues.
- Skips failed tracks but logs warnings.
- Adds Language column for Hindi/Marathi CSVs.
"""
from __future__ import annotations
import os
import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ----------------------------
# Auth
# ----------------------------
HARDCODED_CLIENT_ID = "79293409499a4b08b1d0a409b386c3f3"
HARDCODED_CLIENT_SECRET = "edf8197acdc546268f1d2d4d1f302af3"


def get_spotify_client() -> spotipy.Spotify:
    client_id = os.getenv("SPOTIPY_CLIENT_ID", HARDCODED_CLIENT_ID)
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET", HARDCODED_CLIENT_SECRET)
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

# ----------------------------
# Emotion mapping and playlists
# ----------------------------
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

hindi_playlists = {
    # 0: "3JNWpteYvH3ynMcyPcvxfx",
    # 1: "2uEODdOqnVjn2I7hFyam6C",
    # 2: "47kshOGLVWdwvyO3TQZq3M",
    # 3: "6mMJ2cs48LRYOhvlLabNeB",
    # 4: "44YDp4eCFJedE5QPRzGXPd",
    # 5: "189Sow1xr7R94oSKs4kISc",
    # 6: "7vatYrf39uVaZ8G2cVtEik",
}

marathi_playlists = {
    0: "7MpvyfpjyPwGIt2nKzKQuR",
    1: "50lW60a58GMjNNtRbmqewq",
    2: "1U7L1pk7QySuOaHnXKdHyX",
    3: "2f2JMAHAoP4yOFhgTQe9Ml",
    4: "7yeZpYvhr9lQ1XSehoKbSb",
    5: "1njcuK7i3zuocjYxBgMMgn",
    6: "5dKWOIUR0lmN5URKUVpV6a",
}

# ----------------------------
# Helpers
# ----------------------------
def getTrackIDs(sp: spotipy.Spotify, playlist_id: str):
    track_ids = []
    try:
        playlist = sp.playlist(playlist_id)
    except spotipy.exceptions.SpotifyException as e:
        print(f"  Error fetching playlist {playlist_id}: {e}")
        return track_ids  # return empty list

    for item in playlist['tracks']['items']:
        track = item.get('track')
        if track and track.get('id'):
            track_ids.append(track['id'])

    results = playlist['tracks']
    while results.get('next'):
        try:
            results = sp.next(results)
        except Exception as e:
            print(f"  Warning: failed to fetch next page of tracks: {e}")
            break
        for item in results['items']:
            track = item.get('track')
            if track and track.get('id'):
                track_ids.append(track['id'])
    return track_ids


def getTrackFeatures(sp: spotipy.Spotify, id: str):
    track_info = sp.track(id)
    name = track_info['name']
    album = track_info['album']['name']
    artist = track_info['album']['artists'][0]['name']
    track_url = track_info['external_urls']['spotify']
    return [name, album, artist, track_url]


def emotion_file_name(index: int) -> str:
    return emotion_dict[index].lower()


# ----------------------------
# CSV Generator
# ----------------------------
def generate_language(sp: spotipy.Spotify, playlists_map: dict[int, str], language_suffix: str | None):
    for idx in range(7):
        playlist_id = playlists_map.get(idx)
        if not playlist_id:
            print(f"Skipping emotion index {idx}: no playlist configured")
            continue

        print(f"Fetching {emotion_dict[idx]} from playlist {playlist_id}...")
        track_ids = getTrackIDs(sp, playlist_id)
        if not track_ids:
            print(f"No tracks found for {emotion_dict[idx]}. Skipping file write.")
            continue

        track_list = []
        for tid in track_ids:
            try:
                time.sleep(0.2)
                track_list.append(getTrackFeatures(sp, tid))
            except Exception as e:
                print(f"  Warn: failed track {tid}: {e}")

        if not track_list:
            print(f"No valid tracks for {emotion_dict[idx]}. Skipping file write.")
            continue

        df = pd.DataFrame(track_list, columns=['Name','Album','Artist','URL'])
        if language_suffix:
            df['Language'] = language_suffix
            out_name = f"{emotion_file_name(idx)}_{language_suffix}.csv"
        else:
            out_name = f"{emotion_file_name(idx)}.csv"

        songs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'songs')
        os.makedirs(songs_dir, exist_ok=True)
        out_path = os.path.join(songs_dir, out_name)
        df.to_csv(out_path, index=False)
        print(f"CSV Generated -> {out_path}")


# ----------------------------
# Main
# ----------------------------
def main():
    sp = get_spotify_client()
    generate_language(sp, hindi_playlists, language_suffix="hindi")
    generate_language(sp, marathi_playlists, language_suffix="marathi")


if __name__ == "__main__":
    main()
