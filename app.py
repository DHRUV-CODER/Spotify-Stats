import time
import requests
from flask import Flask, render_template
from environs import Env
import json
env = Env()
app = Flask(__name__)
current_track_info = "https://api.spotify.com/v1/me/player/currently-playing"
auth = env.str("auth") #Go here and get your token -> https://developer.spotify.com/console/get-users-currently-playing-track/
#		$export auth=<key>
current_music="{}"
current_music=json.loads(current_music)
@app.route('/')
def spotify_reg():
    global current_music
    res = requests.get(current_track_info, params={'market': 'ES'}, headers={
        "Authorization": f"Bearer {auth}"}).json()
    current_music = res['item']['album']['name']
    author = res['item']['artists'][0]['name']
    Img = res['item']['album']['images'][1]['url']
    return render_template('stats.html', cm=current_music, author=author, img=Img)


@app.route('/state')
def check():
    res = requests.get(current_track_info, params={'market': 'ES'}, headers={"Authorization": f"Bearer {auth}"}).json()
    cm = res['item']['album']['name']
    if cm!=current_music:
        print("song changed")
        resp='''{"state":"changed"}'''
    else:
        resp='''{"state":"same"}'''
    return resp


if __name__ == "__main__":
    app.run(debug=True)
