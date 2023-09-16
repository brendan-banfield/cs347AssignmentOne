
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
    global capturedX
    global capturedO
    capturedX = capturedO = 0
    newBoard = '-' * 361
    boards[gameId] = f"x#{newBoard}#0#0"
    if player == 'o':
        doComputerMove(gameId)
    output = {'ID': gameId, 'state': boards[gameId]}
    gameId += 1

    return json.dumps(output) + "<br>" + getFormattedBoard(gameId-1)

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
        newScore = str(int(boards[gameId][-3]) + 1)
        boards[gameId] = boards[gameId][:-3] + newScore + boards[gameId][-2:]
    else:
        newScore = str(int(boards[gameId][-1]) + 1)
        boards[gameId] = boards[gameId][:-1] + newScore

def doCaptures(gameId, row, col, player):
    if player == 'x':
        opponent = 'o'
    else:
        opponent = 'x'

    if row <= 15 and getSquare(gameId, row + 1, col) == opponent and getSquare(gameId, row + 2, col) == opponent and getSquare(gameId, row + 3, col) == player:
        setSquare(gameId, row + 1, col, '-')
        setSquare(gameId, row + 2, col, '-')
        recordCapture(gameId, player)

    if col <= 15 and getSquare(gameId, row, col + 1) == opponent and getSquare(gameId, row, col + 2) == opponent and getSquare(gameId, row, col + 3) == player:
        setSquare(gameId, row, col + 1, '-')
        setSquare(gameId, row, col + 2, '-')
        recordCapture(gameId, player)
        
    if row >= 3 and getSquare(gameId, row - 1, col) == opponent and getSquare(gameId, row - 2, col) == opponent and getSquare(gameId, row - 3, col) == player:
        setSquare(gameId, row - 1, col, '-')
        setSquare(gameId, row - 2, col, '-')
        recordCapture(gameId, player)

    if row >= 3 and getSquare(gameId, row, col - 1) == opponent and getSquare(gameId, row, col - 2) == opponent and getSquare(gameId, row, col - 3) == player:
        setSquare(gameId, row, col - 1, '-')
        setSquare(gameId, row, col - 2, '-')
        recordCapture(gameId, player)

    if row <= 15 and col <= 15 and getSquare(gameId, row + 1, col + 1) == opponent and getSquare(gameId, row + 2, col + 2) == opponent and getSquare(gameId, row + 3, col + 3) == player:
        setSquare(gameId, row + 1, col + 1, '-')
        setSquare(gameId, row + 2, col + 2, '-')
        recordCapture(gameId, player)

    if row >= 3 and col <= 15 and getSquare(gameId, row - 1, col + 1) == opponent and getSquare(gameId, row - 2, col + 2) == opponent and getSquare(gameId, row - 3, col + 3) == player:
        setSquare(gameId, row - 1, col + 1, '-')
        setSquare(gameId, row - 2, col + 2, '-')
        recordCapture(gameId, player)

    if row <= 15 and col >= 3 and getSquare(gameId, row + 1, col - 1) == opponent and getSquare(gameId, row + 2, col - 2) == opponent and getSquare(gameId, row + 3, col - 3) == player:
        setSquare(gameId, row + 1, col - 1, '-')
        setSquare(gameId, row + 2, col - 2, '-')
        recordCapture(gameId, player)

    if row >= 3 and col >= 3 and getSquare(gameId, row - 1, col - 1) == opponent and getSquare(gameId, row - 2, col - 2) == opponent and getSquare(gameId, row - 3, col - 3) == player:
        setSquare(gameId, row - 1, col - 1, '-')
        setSquare(gameId, row - 2, col - 2, '-')
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
    move = legalMoves[random.randint(0, len(legalMoves)-1)]
    doMove(gameId, move[0], move[1])

def getFormattedBoard(gameId):
    squares = boards[gameId][2:-4].replace("-", "_")
    lines = [" ".join(list(squares[19 * i: 19 * i + 19]) + [str(i+1)]) for i in range(19)]
    lines.append("0 " * 9 + "1 " * 10)
    lines.append(" ".join([str(i % 10) for i in range(1, 20)]))
    return "<br>".join(lines)


@app.route("/nextmove/<int:gameId>/<int:row>/<int:column>")
def nextmove(gameId, row, column):
    row -= 1
    column -= 1
    global boards
    if gameId not in boards or row < 0 or row >= 19 or column < 0 or column >= 19 or getSquare(gameId, row, column) != "-":
        return nextmoveHelp()
    #setSquare(gameId, row, column, 'O')
    doMove(gameId, row, column)
    doComputerMove(gameId)
    return json.dumps({'ID': gameId, 'row': row, 'column': column, 'state': boards[gameId]}) + "<br>" + getFormattedBoard(gameId)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)