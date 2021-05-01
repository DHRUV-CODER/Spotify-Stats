import time
import requests
from flask import Flask, render_template
import json
from environs import Env
import json
env = Env()
app = Flask(__name__)
current_track_info = "https://api.spotify.com/v1/me/player/currently-playing"
auth = env.str("auth") #Go here and get your token -> https://developer.spotify.com/console/get-users-currently-playing-track/
#		$export auth=<key>
Current_Music="{}"
Current_Music=json.loads(Current_Music)
@app.route('/')
def spotify_reg():
    global Current_Music
    res = requests.get(current_track_info, params={'market': 'ES'}, headers={
        "Authorization": f"Bearer {auth}"}).json()
    Current_Music = res['item']['album']['name']
    Music_Link = res['item']['album']['external_urls']['spotify']
    Author_of_music = res['item']['artists'][0]['name']
    Image_Preview_of_Song = res['item']['album']['images'][1]['url']
    return render_template('stats.html', cm=Current_Music, author=Author_of_music, img=Image_Preview_of_Song,link = Music_Link)

@app.route('/state')
def check():
    res = requests.get(current_track_info, params={'market': 'ES'}, headers={"Authorization": f"Bearer {auth}"}).json()
    cm = res['item']['album']['name']
    if cm!=Current_Music:
        print("song changed")
        resp='''{"state":"changed"}'''
    else:
        resp='''{"state":"same"}'''
    return resp


if __name__ == "__main__":
    app.run(debug=True)
