# Main application file for Emotion-Based Music Recommendation System
from flask import Flask, render_template, Response, jsonify, request, send_from_directory, session, redirect, url_for
from camera import *
from database import EmotionMusicDatabase
import pandas as pd
import os
import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__, static_folder='static')
app.secret_key = 'dev-secret-change-me'  # TODO: move to env

# Spotify OAuth setup
client_id = '79293409499a4b08b1d0a409b386c3f3'
client_secret = 'edf8197acdc546268f1d2d4d1f302af3'
redirect_uri = 'http://127.0.0.1:5000/callback'
scope = 'user-read-private user-read-email streaming'
oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

# Initialize database
db = EmotionMusicDatabase()

# Start a session when the app starts
current_session_id = db.start_session()

headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)

@app.route('/')
def landing():
    # If preferences already set, go to main interface
    if session.get('age_group') and session.get('language_pref'):
        return redirect(url_for('index'))
    return render_template('landing.html')

@app.route('/preferences')
def preferences():
    # Clear saved preferences and show selection page again
    session.pop('age_group', None)
    session.pop('language_pref', None)
    return render_template('landing.html')

@app.route('/start', methods=['POST'])
def start():
    # Save user preferences
    session['age_group'] = request.form.get('age_group')
    session['language_pref'] = request.form.get('language_pref')
    return redirect(url_for('index'))

@app.route('/home')
def index():
    # Main UI after preferences
    prefs = {
        'age_group': session.get('age_group', 'unknown'),
        'language_pref': session.get('language_pref', 'random'),
    }
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1, prefs=prefs)

df1 = pd.DataFrame({
    'SongName': [
        'Blinding Lights - The Weeknd', 
        'Levitating - Dua Lipa', 
        'Shape of You - Ed Sheeran', 
        'Stay - The Kid LAROI, Justin Bieber', 
        'Save Your Tears - The Weeknd', 
        'Good 4 U - Olivia Rodrigo', 
        'Industry Baby - Lil Nas X, Jack Harlow', 
        'Kiss Me More - Doja Cat, SZA', 
        'Montero (Call Me By Your Name) - Lil Nas X', 
        'Peaches - Justin Bieber, Daniel Caesar, Giveon', 
        'Heat Waves - Glass Animals', 
        'Butter - BTS', 
        'Bad Habits - Ed Sheeran', 
        'Don’t Start Now - Dua Lipa', 
        'As It Was - Harry Styles'
    ]
})

# Assign Spotify URLs for the songs
df1['SpotifyUrl'] = [
    'https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b',
    'https://open.spotify.com/track/0GLTt9qKb19NsxFhjdUWL0',
    'https://open.spotify.com/track/7qiZfU4dY1lWllzX7nJ2Xa',
    'https://open.spotify.com/track/0yS9gSgwzHsRUfgGz1vs5d',
    'https://open.spotify.com/track/4cK3p0Ws4gF4fn0zv6Ujb6',
    'https://open.spotify.com/track/5fV9hpx5M2oVOFppc1Ml8X',
    'https://open.spotify.com/track/1qlF9a7I74H2guwTYg6Jeq',
    'https://open.spotify.com/track/1j6J9s5duHeKiON2wBbbbl',
    'https://open.spotify.com/track/4mNoFKNZtJl93Do0zwmuLV',
    'https://open.spotify.com/track/1XsPLZnyM7tQNUotNniWNm',
    'https://open.spotify.com/track/5Pjj1EFOd3r0sc2kYQHvs5',
    'https://open.spotify.com/track/7l6W2uYTcXq8GsqwQVuTfH',
    'https://open.spotify.com/track/4ud5nUmX1gG4l5DgHD44g6',
    'https://open.spotify.com/track/0xnH9Vcd5biQUoQk0Pfugf',
    'https://open.spotify.com/track/4HJ7S7yqxAbo9fM4kw4Xgl'
]

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

@app.route('/get_emotion')
def get_emotion():
    # Get the current emotion from the global variable in camera.py
    current_emotion = emotion_dict.get(show_text[0], "Unknown")
    
    # Log the emotion in the database
    emotion_id = db.log_emotion(current_emotion)
    
    # Increment the emotion count for the current session
    if current_session_id and emotion_id:
        db.increment_emotion_count(current_session_id)
    
    return jsonify({"emotion": current_emotion})

@app.route('/get_recommendations')
def get_recommendations():
    emotion = request.args.get('emotion', '')

    # Map emotion name to index (fallback to Neutral)
    emotion_index = next((i for i, e in emotion_dict.items() if e.lower() == emotion.lower()), 4)

    # Resolve base CSV path for the detected emotion
    lang_pref = (session.get('language_pref') or 'english').lower()
    age_pref = session.get('age_group', 'unknown')
    base_path = music_dist[emotion_index]
    root, ext = os.path.splitext(base_path)

    # Strict language-specific CSV selection
    # - english -> base file (e.g., happy.csv)
    # - hindi/marathi -> language-specific files (e.g., happy_hindi.csv / happy_marathi.csv)
    if lang_pref in ('hindi', 'marathi'):
        csv_path = f"{root}_{lang_pref}{ext}"
    else:
        csv_path = base_path

    # Final safety fallback to base file if specific file doesn't exist
    if not os.path.exists(csv_path):
        csv_path = base_path

    # Load recommendations
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV '{csv_path}': {e}")
        return jsonify([])

    # Optional age group bias (example heuristic: prefer clean tracks for kids)
    age_group = session.get('age_group', 'unknown')
    if age_group == 'kid' and 'Name' in df.columns:
        df = df[~df['Name'].str.contains('explicit', case=False, na=False)]

    df = df.head(10)  # Limit to 10 recommendations

    # Prepare response data
    recommendations = []
    for _, row in df.iterrows():
        # Extract and sanitize values
        name = str((row.get('Name') if isinstance(row, dict) else row.get('Name', ''))).strip()
        artist = str((row.get('Artist') if isinstance(row, dict) else row.get('Artist', ''))).strip()
        link = str((row.get('URL') if isinstance(row, dict) else row.get('URL', ''))).strip()

        # Skip if any required field is missing/invalid (except URL; we'll fallback to search link)
        if not name or name.lower() == 'nan':
            continue
        if not artist or artist.lower() == 'nan':
            continue

        # If URL missing, fallback to Spotify search link so rows still show up
        if not (isinstance(link, str) and link.startswith('http')):
            try:
                from urllib.parse import quote_plus
                query = name + (f" {artist}" if artist else "")
                link = f"https://open.spotify.com/search/{quote_plus(query)}"
            except Exception:
                # As a last resort, skip if we cannot construct a link
                continue

        # Add Spotify URI if applicable
        uri = None
        if link.startswith('https://open.spotify.com/track/'):
            track_id = link.split('/')[-1].split('?')[0]
            uri = f'spotify:track:{track_id}'

        song_data = {"name": name, "artist": artist, "link": link, "uri": uri}
        recommendations.append(song_data)

        # Log recommendation in database if emotion is tracked
        if emotion:
            try:
                emotion_id = db.log_emotion(emotion)
                db.log_recommendation(emotion_id, name, artist, link)
            except Exception as e:
                print(f"Error logging recommendation: {e}")
                # Continue without stopping the recommendation process

    return jsonify(recommendations)

@app.route('/history')
def history():
    # Get emotion and recommendation history
    emotion_history = db.get_emotion_history(20)
    recommendation_history = db.get_recommendation_history(20)
    emotion_stats = db.get_emotion_stats()
    
    return render_template('history.html', 
                          emotion_history=emotion_history,
                          recommendation_history=recommendation_history,
                          emotion_stats=emotion_stats)

@app.route('/api/history')
def api_history():
    # Get emotion and recommendation history as JSON
    emotion_history = db.get_emotion_history(20)
    recommendation_history = db.get_recommendation_history(20)
    emotion_stats = db.get_emotion_stats()
    
    return jsonify({
        "emotion_history": emotion_history,
        "recommendation_history": recommendation_history,
        "emotion_stats": emotion_stats
    })

def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        token_info = oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    return token_info

@app.route('/login')
def login():
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/get_token')
def get_token_route():
    token_info = get_token()
    if token_info:
        return jsonify({'access_token': token_info['access_token']})
    return jsonify({'error': 'Not authenticated'}), 401

@app.route('/logout')
def logout():
    session.pop('token_info', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        app.debug = True
        app.run()
    finally:
        # End the session when the app stops
        if current_session_id:
            db.end_session(current_session_id)
        # Close the database connection
        db.close()