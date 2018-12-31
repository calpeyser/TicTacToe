import flask, json

from ..player import RandomPlayer

app = flask.Flask(__name__)
player = RandomPlayer("O")

@app.route("/")
def index():
	return flask.redirect(flask.url_for("static", filename="index.html"))

@app.route("/move", methods=['POST'])
def move():
	state = json.loads(flask.request.form['state'])
	move = player.move(state)
	return move
