from flask import Flask, request, render_template
from GamePriceBot import steambot
from GamePriceBot import epicbot
import json

app = Flask(__name__)

@app.route("/")
def frontpage():
    return render_template("frontend.html")

@app.route('/search',methods = ['POST', 'GET'])
def search():
    game = request.form['gamename']
    steamdata = steambot(game)
    epicdata = epicbot(game)
    rd = {'steamdata':steamdata,'epicdata':epicdata}
    gamedata = json.dumps(rd)
    return gamedata

if __name__ == '__main__':
    app.run(debug = False)