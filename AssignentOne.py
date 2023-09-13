import flask
import json
app = flask.Flask(__name__)

boards = {}
gameId = 0

@app.route("/newgame")
def newGameHelp():
    return "Usage: http://localhost:5000/newgame/<player>, where <player> is x or o"

@app.route("/newgame/<player>")
def newgame(player):
    if player.lower() not in ['x', 'o']:
        return newGameHelp()
    global boards
    global gameId
    newBoard = '-' * 361
    boards[gameId] = f"{player}#{newBoard}#0#0"
    output = {'ID': gameId, 'state': f"{player}#{newBoard}#0#0"}
    gameId += 1

    return json.dumps(output)

@app.route("/nextmove/")
def nextmoveHelp():
    return "Usage: http://localhost:5000/nextmove/gameID/row/col, where:<br>-gameID is a previously created game<br>-row and column are a legal move space"

@app.route("/nextmove/<gameID>/<row>/<column>")
def nextmove(gameId, row, column):
    global boards
    if gameId not in boards:
        return 
    pass




if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)