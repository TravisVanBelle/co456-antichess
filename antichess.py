import chess
import sys

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

def weMove(board):
    legalMoves = getLegalMoves(board)

    board.push(legalMoves[0])

def otherPlayerMoves(board):
    move = raw_input() # assume input is valid
    move = chess.Move.from_uci(move)

    assert move in board.legal_moves

    board.push(move)

def main(argv):
    color = argv[1] # 'black' or 'white'

    board = chess.Board()

    if (color == "black"): # other player goes first
        otherPlayerMoves(board)

    while (not(board.is_game_over())):
        weMove(board)

        print(board)

        otherPlayerMoves(board)


main(sys.argv)
