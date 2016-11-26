import chess

surroundingSquaresMap = {
    'l': -1,
    'r': -1,
    'u': -1,
    'd': -1,
    'lu': -1,
    'ru': -1,
    'ld': -1,
    'rd': -1
}

def getLegalMoves(board):
    captureMoves = list()
    legalMoves = list()

    for move in board.legal_moves:
        legalMoves.append(move)

        if (board.is_capture(move)):
            captureMoves.append(move)

    if (len(captureMoves) > 0):
        return captureMoves
    else:
        return legalMoves

# Checks if square1 is closer to the other side than square2
def isSquareAhead(square1, square2, color):
    # Start at bottom part of board
    if (color == chess.WHITE):
        return square1 >= square2 + (8 - square2%8)
    # Start at top of board
    else:
        return square1 < square2 - square2%8

# Gets the values of the 8 squares surrounding the given square
def getSurroundingSquares(square):
    squares = surroundingSquaresMap.copy()

    # Left squares
    if (square%8 != 0):
        squares['l'] = (square-1)
        if (square > 7):
            squares['ld'] = (square-9)
        if (square < 56):
            squares['lu'] = (square+7)
    # Right squares
    if (square%8 != 7):
        squares['r'] = (square+1)
        if (square > 7):
            squares['rd'] = (square-7)
        if (square < 56):
            squares['ru'] = (square+9)
    # Top and Bottom squares
    if (square > 7):
        squares['d'] = (square-8)
    if (square < 56):
        squares['u'] = (square+8)

    return squares
