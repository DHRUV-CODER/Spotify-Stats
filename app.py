from flask import Flask, request, url_for, session, redirect, render_template
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
app = Flask(__name__)

app.secret_key = "some-key"
TOKEN_INFO = "token-info"
SCOPE = "user-read-currently-playing"
Current_Music="{}"
Current_Music=json.loads(Current_Music)

@app.before_request
def before_request():
    if os.path.exists(".cache"):
        os.remove(".cache")

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def authorize():
    sp_auth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    
    token_info = sp_auth.get_access_token(code=code)
    session['token_info'] = token_info
    return redirect(url_for('info',_external=True,_scheme = 'https'))


def get_token(session):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        # Don't reuse a SpotifyOAuth object because they store token info and you could leak user tokens if you reuse a SpotifyOAuth object
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


@app.route('/info')
def info():
    global Current_Music
    session['token_info'], authorized = get_token(session)
    session.modified = True
    if not authorized:
        return redirect(url_for('login', _external=False,_scheme = 'https'))

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    
    res = sp.currently_playing()
    
    try:
        Current_Music = res['item']['album']['name']
        Music_Link = res['item']['album']['external_urls']['spotify']
        Author_of_music = res['item']['artists'][0]['name']
        Image_Preview_of_Song = res['item']['album']['images'][1]['url']
    except:
        Current_Music = "No Music"
        Music_Link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        Author_of_music = "No One"
        Image_Preview_of_Song = "https://cdn2.iconfinder.com/data/icons/dashboard-website/24/amount_Copy_3-512.png"
        
    return render_template('index.html', cm=Current_Music, author=Author_of_music, img=Image_Preview_of_Song,link = Music_Link)
    
    
    return render_template('index.html',)
 
@app.route('/state')
def check():
    session['token_info'], authorized = get_token(session)
    session.modified = True
    
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
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
        client_id="",
        client_secret="",
        redirect_uri=url_for('authorize', _external=True,_scheme = 'https'),
        scope=SCOPE)


if __name__ == "__main__":
    app.run(debug=True)


