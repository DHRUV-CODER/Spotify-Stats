from flask import Flask, request, url_for, session, redirect, render_template
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
app = Flask(__name__)

app.secret_key = "something-random"
app.config['SESSION_COOKIE_NAME'] = "Dhruv's Cookie"
TOKEN_INFO = "token-info"
Current_Music="{}"
Current_Music=json.loads(Current_Music)

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('spotify_reg', _external=True))




def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

@app.route('/stats')
def spotify_reg():
    global Current_Music
    try:
        token_info = get_token()
    except:
        print("Not Logged In")
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    res = sp.currently_playing()
    Current_Music = res['item']['album']['name']
    Music_Link = res['item']['album']['external_urls']['spotify']
    Author_of_music = res['item']['artists'][0]['name']
    Image_Preview_of_Song = res['item']['album']['images'][1]['url']
    return render_template('stats.html', cm=Current_Music, author=Author_of_music, img=Image_Preview_of_Song,link = Music_Link)

@app.route('/state')
def check():
    try:
        token_info = get_token()
    except:
        print("Not Logged In")
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    res = sp.currently_playing()
    cm = res['item']['album']['name']
    if cm!=Current_Music:
        print("song changed")
        resp='''{"state":"changed"}'''
    else:
        resp='''{"state":"same"}'''
    return resp


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="client_id",
        client_secret="client_secreat",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-read-currently-playing")


if __name__ == "__main__":
    app.run(debug=True)
