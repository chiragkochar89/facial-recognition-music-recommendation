# from flask import Flask, render_template, Response, jsonify
# import pandas as pd
# from camera import *  # Assuming this handles the video feed

# app = Flask(__name__)

# headings = ("Song Name", "Album", "Artist", "Spotify Link", "Open in New Window")
# df1 = music_rec()
# df1 = df1.head(15)  # Keep only first 15 songs

# @app.route('/')
# def index():
#     print(df1.to_json(orient='records'))
#     return render_template('index.html', headings=headings, data=df1)

# df1 = pd.DataFrame({
#     'SongName': [
#         'Blinding Lights - The Weeknd', 
#         'Levitating - Dua Lipa', 
#         'Shape of You - Ed Sheeran', 
#         'Stay - The Kid LAROI, Justin Bieber', 
#         'Save Your Tears - The Weeknd', 
#         'Good 4 U - Olivia Rodrigo', 
#         'Industry Baby - Lil Nas X, Jack Harlow', 
#         'Excuses - AP Dhillon, gill', 
#         'Brown Munde - Gminxr ,AP Dhillon', 
#         'Khatam - Emiway Bantai', 
#         'We Rollin - Shubh', 
#         '295 - Sidhu Moose Wala', 
#         'Yalgar- CarryMinati', 
#         'SPACESHIP - AP Dhillon, Shinda Kahlon', 
#         'As It Was - Harry Styles'
#     ],
#     'Album': [
#         'After Hours', 'Future Nostalgia', 'Divide', 'F*ck Love', 'After Hours', 
#         'SOUR', 'Montero', 'Planet Her', 'Montero', 'Justice', 'Heat Waves', 
#         'Butter', 'Equals', 'Future Nostalgia', 'Harry\'s House'
#     ],
#     'Artist': [
#         'The Weeknd', 'Dua Lipa', 'Ed Sheeran', 'The Kid LAROI, Justin Bieber', 'The Weeknd', 
#         'Olivia Rodrigo', 'Lil Nas X, Jack Harlow', 'Doja Cat, SZA', 'Lil Nas X', 'Justin Bieber, Daniel Caesar, Giveon', 
#         'Glass Animals', 'BTS', 'Ed Sheeran', 'Dua Lipa', 'Harry Styles'
#     ]
# })

# # Assign Spotify URLs for the songs
# df1['SpotifyUrl'] = [
#     'https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b?si=662177839521475a',
#     'https://open.spotify.com/track/39LLxExYz6ewLAcYrzQQyP?si=fd590ae404c84b36',
#     'https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3?si=b21aeb3414244152',
#     'https://open.spotify.com/track/5HCyWlXZPP0y6Gqq8TgA20?si=d167b93b561746db',
#     'https://open.spotify.com/track/4ZtFanR9U6ndgddUvNcjcG?si=35c8f69e3f4f4e8f',
#     'https://open.spotify.com/track/27NovPIUIRrOZoCHxABJwK?si=6daa934782ea4cac',
#     'https://open.spotify.com/track/29m79w9xPMH4YCD6r8JSmV?si=2da43c198b8f44d8',
#     'https://open.spotify.com/track/58f4twRnbZOOVUhMUpplJ4?si=7bda9bf9084d4830',
#     'https://open.spotify.com/track/251VdhnEdo9kxdQ7xeGuc3?si=c3f4a69180ed4c28',
#     'https://open.spotify.com/track/6ZYxNjuAU9Vy3VtF6W1dtE?si=2c2dc410be5049d8',
#     'https://open.spotify.com/track/5W7DOVGQLTigu09afW7QMT?si=429f8d716bed4508',
#     'https://open.spotify.com/track/0RGp4KA9wvndxqPIWoKwnD?si=c71b08b8c51f4265',
#     'https://open.spotify.com/track/0RGp4KA9wvndxqPIWoKwnD?si=e85e8f9e62f440ca',
#     'https://open.spotify.com/track/2PcGqmKToUz0s65q1Acg7d?si=3fd8ba13abaf4ce9',
#     'https://open.spotify.com/track/4Dvkj6JhhA12EX05fT7y2e?si=835c23bf18ca417d'
# ]

# def gen(camera):
#     while True:
#         global df1
#         frame, df1 = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/t')
# def gen_table():
#     return df1.to_json(orient='records')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()


# ----------------------------------------------------------------------------if anything dosent work uncommend this ------------------------------------
from flask import Flask, render_template, Response, jsonify 
import gunicorn
from camera import *

app = Flask(__name__)

headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)

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

if __name__ == '__main__':
    app.debug = True
    app.run()