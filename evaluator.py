import chess
from helpers import *

valueMap = {
    1: 1,           #Pawn
    2: 3,           #Knight
    3: 3,           #Bishop
    4: 5,           #Rook
    5: 9,           #Queen
    #6: float("inf") #King
}

oddSquares = [
    0, 2, 4, 6,
    9, 11, 13, 15,
    16, 18, 20, 22,
    25, 27, 29, 31,
    32, 34, 36, 38,
    41, 43, 45, 47,
    48, 50, 52, 54,
    57, 59, 61, 63
]

evenSquares = [
    1, 3, 5, 7,
    8, 10, 12, 14,
    17, 19, 21, 23,
    24, 26, 28, 30,
    33, 35, 37, 39,
    40, 42, 44, 46,
    49, 51, 53, 55,
    56, 58, 60, 62
]

boardPieces = {
    1: [], # White
    0: []  # Black
}

# Sets boardPieces object to all pieces the players have
def setPieceLists(board):
    boardPieces[0] = list()
    boardPieces[1] = list()
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if (not(piece)):
            continue

        boardPieces[piece.color].append((square, piece))

#### MATERIAL POSITION EVALUATION ####
def materialPositionEvaluation(board, color):
    value1 = 0
    value2 = 0

    for piece in boardPieces[color]:
        value1 += getPositionValue(piece[1].piece_type, piece[0], color)

    for piece in boardPieces[not(color)]:
        value2 += getPositionValue(piece[1].piece_type, piece[0], not(color))

    return value1 - value2

#### KING PROTECTION EVALUATION ####
def kingProtectionEvaluation(board, color):
    value1 = singleKingProtectionEvaluation(board,color)
    value2 = singleKingProtectionEvaluation(board,not(color))

    return value1 - value2

def singleKingProtectionEvaluation(board, color):
    kingPosition = 0
    value = 0

    # Find position of King for given color
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if (not(piece)):
            continue
        if (piece.piece_type == chess.KING and piece.color == color):
            kingPosition = square

    # Get map of squares surrounding the King
    surroundingSquares = getSurroundingSquares(kingPosition)

    for key in surroundingSquares:
        square = surroundingSquares[key]

        if (square == -1):
            continue

        piece = board.piece_at(square)
        if (piece and piece.color == color):
            if (isSquareAhead(square, kingPosition, color)):
                value += 1
            else:
                value += 0.25

    theirBishop = chess.Piece(chess.BISHOP, not(color))
    theirBishops = [item for item in boardPieces[not(color)] if item[1] == theirBishop]
    for bishop in theirBishops:
        if (kingPosition in oddSquares and bishop[0] in oddSquares):
            value -= 0.5
        elif (kingPosition in evenSquares and bishop[0] in evenSquares):
            value -= 0.5

    return value

#### PAWN TRAP EVALUATION ####
def pawnTrapEvaluation(board, color):
    value1 = singlePawnTrapEvaluation(board, color)
    value2 = singlePawnTrapEvaluation(board, not(color))

    return value1 - value2

def singlePawnTrapEvaluation(board, color):
    value = 0

    for piece in boardPieces[color]:
        if (piece[1].piece_type != chess.PAWN):
            continue

        surroundingSquares = getSurroundingSquares(piece[0])
        if (color == chess.WHITE):
            lu = board.piece_at(surroundingSquares['lu'])
            ru = board.piece_at(surroundingSquares['ru'])
            if (lu and lu.piece_type == chess.PAWN):
                value += 1
            if (ru and ru.piece_type == chess.PAWN):
                value += 1
        if (color == chess.BLACK):
            ld = board.piece_at(surroundingSquares['ld'])
            rd = board.piece_at(surroundingSquares['rd'])
            if (ld and ld.piece_type == chess.PAWN):
                value += 1
            if (rd and rd.piece_type == chess.PAWN):
                value += 1

    return value

#### MATERUAL EVALUATION ####
def materialEvaluation(board, color):
    black = {
        'count': 0,
        'bishops': 0,
        'pawns': 0,
        'knights': 0
    }
    white = {
        'count': 0,
        'bishops': 0,
        'pawns': 0,
        'knights': 0
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if (not(piece) or (piece.piece_type == 6)):
            continue

        pieceValue = valueMap[piece.piece_type]
        if (piece.color == chess.BLACK):
            black['count'] += pieceValue
            if (piece.piece_type == chess.BISHOP):
                black['bishops'] += 1
            elif (piece.piece_type == chess.PAWN):
                black['pawns'] += 1
            elif (piece.piece_type == chess.KNIGHT):
                black['knights'] += 1
        else:
            white['count'] += pieceValue
            if (piece.piece_type == chess.BISHOP):
                white['bishops'] += 1
            elif (piece.piece_type == chess.PAWN):
                white['pawns'] += 1
            elif (piece.piece_type == chess.KNIGHT):
                white['knights'] += 1

    if (black['bishops'] == 2):
        black['count'] += 0.5
    if (white['bishops'] == 2):
        white['count'] += 0.5
    if (black['pawns'] >= 2):
        black['count'] += 0.5
    if (white['pawns'] >= 2):
        white['count'] += 0.5
    if (black['pawns'] >= 4 and black['knights'] == 2):
        black['count'] += 0.5
    if (white['pawns'] >= 4 and white['knights'] == 2):
        white['count'] += 0.5

    if (color == chess.BLACK):
        return black['count'] - white['count']
    else:
        return white['count'] - black['count']

# Returns the complete evaluation for a given board
def getEvaluation(board, color):
    setPieceLists(board)

    m = materialEvaluation(board, color)
    rk = kingProtectionEvaluation(board, color)
    pt = pawnTrapEvaluation(board, color)
    mp = materialPositionEvaluation(board, color)

    return {
        'material': m,
        'king': rk,
        'pawn trap': pt,
        'materialposition': mp
    }

# Returns the numerical utility value for a given board and color
# Evaluates assuming its the given color's turn to move
def evaluate(board, color):
    # If the board is a checkmate, there are no moves, this player loses.
    if (board.is_checkmate()):
        return -getEndgameValue()

    # Get the values for the given board
    evaluation = getEvaluation(board, color)

    # Return the utility value for this board
    return evaluation['material']*10000 + evaluation['materialposition']*100 + evaluation['pawn trap']*5;
