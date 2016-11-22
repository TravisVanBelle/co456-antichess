import chess
import sys

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
        # we move

        otherPlayerMoves(board)

main(sys.argv)
