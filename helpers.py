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

positionValues = {
    chess.PAWN: [
         0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20
    ]
}

def log(string):
    print string

def getPositionValue(pieceType, squareNumber, color):
    if (color == chess.WHITE):
        return positionValues[pieceType][63-squareNumber]
    else:
        return positionValues[pieceType][squareNumber]

def getPieceCount(board):
    value = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if (piece):
            value += 1

    return value

def getEndgameValue():
    return 1000000

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
