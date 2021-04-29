import time
import requests
from flask import Flask, render_template
app = Flask(__name__)

current_track_info = "https://api.spotify.com/v1/me/player/currently-playing"
auth = "" #Go here and get your token -> https://developer.spotify.com/console/get-users-currently-playing-track/?market=&additional_types=

@app.route('/')
def spotify_reg():
    res = requests.get(current_track_info, params={'market': 'ES'}, headers={
        "Authorization": f"Bearer {auth}"}).json()
    current_music = res['item']['album']['name']
    author = res['item']['artists'][0]['name']
    Img = res['item']['album']['images'][1]['url']
    return render_template('stats.html', cm=current_music, author=author, img=Img)

    
if __name__ == "__main__":
    app.run(debug=True)



