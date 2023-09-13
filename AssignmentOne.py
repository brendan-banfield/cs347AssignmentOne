
import flask
import json
import random
app = flask.Flask(__name__)

boards = {}
gameId = 0

@app.route("/newgame")
def newGameHelp():
    return "Usage: http://localhost:5000/newgame/player, where player is x or o"

@app.route("/newgame/<player>")
def newgame(player):
    player = player.lower()
    if player not in ['x', 'o']:
        return newGameHelp()
    global boards
    global gameId
    newBoard = '-' * 361
    boards[gameId] = f"x#{newBoard}#0#0"
    if player == 'o':
        doComputerMove(gameId)
    output = {'ID': gameId, 'state': boards[gameId]}
    gameId += 1

    return json.dumps(output)

@app.route("/nextmove/")
def nextmoveHelp():
    return "Usage: http://localhost:5000/nextmove/gameID/row/col, where:<br>-gameID is a previously created game<br>-row and column are a legal move space"

def getSquare(gameId, row, column):
    return boards[gameId][row * 19 + column + 2]

def setSquare(gameId, row, column, newChar):
    idx = row * 19 + column + 2
    boards[gameId] = boards[gameId][:idx] + newChar + boards[gameId][idx + 1:]

def getTurn(gameId):
    return boards[gameId][0]

def changeTurn(gameId):
    turn = getTurn(gameId)
    if turn == 'x':
        boards[gameId] = 'o' + boards[gameId][1:]
    else:
        boards[gameId] = 'x' + boards[gameId][1:]
    

        
def doCaptures(gameId, row, col, player):
    raise NotImplementedError

def doMove(gameId, row, col, player):
    setSquare(gameId, row, col, player)
    doCaptures(gameId, row, col, player)


    raise NotImplementedError


def doComputerMove(gameId):
    legalMoves = []
    for row in range(19):
        for column in range(19):
            if getSquare(gameId, row, column) == '-':
                legalMoves.append((row, column))
    move = legalMoves[random.randint(len(legalMoves))]
    doMove(gameId, move[0], move[1], getTurn(gameId))



@app.route("/nextmove/<int:gameId>/<int:row>/<int:column>")
def nextmove(gameId, row, column):
    global boards
    if gameId not in boards or row < 0 or row >= 19 or column < 0 or column >= 19 or getSquare(gameId, row, column) != "-":
        return nextmoveHelp()
    #setSquare(gameId, row, column, 'O')
    doMove(gameId, row, column, getTurn(gameId))
    return json.dumps({'ID': gameId, 'row': row, 'column': column, 'state': boards[gameId]})


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)