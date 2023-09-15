
import flask
import json
import random
app = flask.Flask(__name__)

boards = {}
gameId = 0
capturedX = 0
capturedO = 0

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
    global capturedX
    global capturedO
    capturedX = capturedO = 0
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
    
def recordCapture(gameId, player):
    if player == 'x':
        capturedX += 1
        board[gameID][2 + (19 * 19) + 2] = str(capturedX)
    else:
        capturedO += 1
        board[gameID][2 + (19 * 19) + 4] = str(capturedO)

def doCaptures(gameId, row, col, player):
    index = row * 19 + col
    if player == 'x':
        opponent = 'o'
    else:
        opponent = 'x'

    if row <= 16 and col <= 16:
        # checks for horizontal capture
        if (board[gameId][index + 2 + 3] == player) and (board[gameId][index + 2 + 1] == board[gameId][index + 2 + 2] == opponent): # +2 to account for the "<turn>#"
            board[gameId][index + 2 + 1] = '-'
            board[gameId][index + 2 + 2] = '-'
            recordCapture(gameId, player)
        # checks for vertical capture
        if (board[gameId][index + 2 + (19 * 3)] == player) and (board[gameId][index + 2 + 19] == board[gameId][index + 2 + (19 * 2)] == opponent):
            board[gameId][index + 2 + 19] = '-'
            board[gameId][index + 2 + (19 * 2)] = '-'
            recordCapture(gameId, player)
        # checks for diagonal capture
        if (board[gameId][index + 2 + 3 + (19 * 3)] == player) and (board[gameId][index + 2 + 1 + 19] == board[gameId][index + 2 + 2 + (19 * 2)] == opponent):
            board[gameId][index + 2 + 1 + 19] = '-'
            board[gameId][index + 2 + 2 + (19 * 2)] = '-'
            recordCapture(gameId, player)

    if row >= 4 and col <= 4:
        # checks for horizontal capture
        if (board[gameId][index + 2 - 3] == player) and (board[gameId][index + 2 - 1] == board[gameId][index + 2 - 2] == opponent): # +2 to account for the "<turn>#"
            board[gameId][index + 2 - 1] = '-'
            board[gameId][index + 2 - 2] = '-'
            recordCapture(gameId, player)
        # checks for vertical capture
        if (board[gameId][index + 2 - (19 * 3)] == player) and (board[gameId][index + 2 - 19] == board[gameId][index + 2 - (19 * 2)] == opponent):
            board[gameId][index + 2 - 19] = '-'
            board[gameId][index + 2 - (19 * 2)] = '-'
            recordCapture(gameId, player)
        # checks for diagonal capture
        if (board[gameId][index + 2 - 3 - (19 * 3)] == player) and (board[gameId][index + 2 - 1 - 19] == board[gameId][index + 2 - 2 - (19 * 2)] == opponent):
            board[gameId][index + 2 - 1 - 19] = '-'
            board[gameId][index + 2 - 2 - (19 * 2)] = '-'
            recordCapture(gameId, player)

def doMove(gameId, row, col):
    turn = getTurn(gameId)
    setSquare(gameId, row, col, turn)
    doCaptures(gameId, row, col, turn)
    changeTurn(gameId)

def doComputerMove(gameId):
    legalMoves = []
    for row in range(19):
        for column in range(19):
            if getSquare(gameId, row, column) == '-':
                legalMoves.append((row, column))
    move = legalMoves[random.randint(len(legalMoves))]
    doMove(gameId, move[0], move[1])




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