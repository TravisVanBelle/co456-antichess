import chess

valueMap = {
    1: 1,           #Pawn
    2: 3,           #Knight
    3: 3,           #Bishop
    4: 5,           #Rook
    5: 9,           #Queen
    #6: float("inf") #King
}

def materialEvaluation(board, color):
    black = 0
    white = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if (not(piece) or (piece.piece_type == 6)):
            continue

        pieceValue = valueMap[piece.piece_type]

        if (piece.color == chess.BLACK):
            black += pieceValue
        else:
            white += pieceValue

    if (color == chess.BLACK):
        return black - white
    else:
        return white - black


# board: A Board object
# color: True=White, False=Black
def evaluate(board, color):
    m = materialEvaluation(board, color)
    return m
