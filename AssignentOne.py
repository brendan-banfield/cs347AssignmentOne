import flask
import json
app = flask.Flask(__name__)


@app.route("/newgame/<player>")
def newgame(x, y):
    pass


@app.route("/nextmove/<gameID>/<row>/<column>")
def nextmove(x, y):
    pass




if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)