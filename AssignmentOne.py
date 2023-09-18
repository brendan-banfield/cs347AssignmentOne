
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
    newBoard = '-' * 19 * 19
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

def isInBounds(row, col):
    if row < 0 or row >= 19:
        return False
    if col < 0 or col >= 19:
        return False
    return True

def getTurn(gameId):
    return boards[gameId][0]

def changeTurn(gameId):
    turn = getTurn(gameId)
    if turn == 'x':
        boards[gameId] = 'o' + boards[gameId][1:]
    else:
        boards[gameId] = 'x' + boards[gameId][1:]

def checkPattern(gameId, start: tuple, direction: tuple, pattern: list) -> bool:
    r, c = start
    dr, dc = direction
    l = len(pattern)
    if not isInBounds(r + (l-1)*dr, c + (l-1)*dc):
        return False
    for i in range(l):
        if getSquare(gameId, r, c) != pattern[i]:
            return False
        r += dr
        c += dc
    return True
        

def getCaptures(gameId, player):
    if player == 'x':
        return int(boards[gameId][2 + 19 * 19 + 1])
    else:
        return int(boards[gameId][2 + 19 * 19 + 3])
    
def recordCapture(gameId, player):
    if player == 'x':
        newScore = str(int(boards[gameId][-3]) + 1)
        boards[gameId] = boards[gameId][:-3] + newScore + boards[gameId][-2:]
    else:
        newScore = str(int(boards[gameId][-1]) + 1)
        boards[gameId] = boards[gameId][:-1] + newScore

def checkCapture(gameId, row, col, direction, player, opponent):
    if checkPattern(gameId, (row, col), direction, [player, opponent, opponent, player]):
        dr, dc = direction
        setSquare(gameId, row + dr, col + dc, '-')
        setSquare(gameId, row + 2*dr, col + 2*dc, '-')
        recordCapture(gameId, player)

def doCaptures(gameId, row, col, player):
    opponent = 'o' if player == 'x' else 'x'
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            checkCapture(gameId, row, col, (i, j), player, opponent)  
    if getCaptures(gameId, player) >= 5:
        displayWin(gameId, player)

    

def doMove(gameId, row, col):
    turn = getTurn(gameId)
    setSquare(gameId, row, col, turn)
    doCaptures(gameId, row, col, turn)
    checkForFiveInARow(gameId, row, col, turn)
    changeTurn(gameId)

def searchForPattern(gameId, pattern):
    captures = []
    for r in range(19):
        for c in range(19):
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    if checkPattern(gameId, (r, c), (dr, dc), pattern):
                        captures.append((r, c))
    return captures

def findGoodMoves(gameId):
    p = getTurn(gameId)
    o = "x" if p == "o" else "o"

    fives = searchForPattern(gameId, ['-', p, p, p, p])
    if len(fives) > 0:
        return fives
    
    fours = searchForPattern(gameId, ['-', p, p, p])
    if len(fours) > 0:
        return fours
    
    threes = searchForPattern(gameId, ['-', p, p])
    if len(threes) > 0:
        return threes
    
    captures = searchForPattern(gameId, ['-', o, o, p])
    if len(captures) > 0:
        return captures
    
    ideas = searchForPattern(gameId, ['-', o]) + searchForPattern(gameId, ['-', p])
    if len(ideas) > 0:
        return ideas
    
    return searchForPattern(gameId, ['-'])
    
    

def doComputerMove(gameId):
    moveChoices = findGoodMoves(gameId)
    move = moveChoices[random.randint(0, len(moveChoices)-1)]
    doMove(gameId, move[0], move[1])

def getFormattedBoard(gameId):
    squares = boards[gameId][2:-4].replace("-", "_")
    lines = [" ".join(list(squares[19 * i: 19 * i + 19]) + [str(i+1)]) for i in range(19)]
    lines.append("0 " * 9 + "1 " * 10)
    lines.append(" ".join([str(i % 10) for i in range(1, 20)]))
    return "<br>".join(lines)

def displayWin(gameId, player):
    raise NotImplementedError

def checkForFiveInARow(gameId, row, col, player):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            if checkPattern(gameId, (row, col), (i, j), [player] * 5):
                displayWin(gameId, player)
 
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