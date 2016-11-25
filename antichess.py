import chess
import sys
import evaluator
from random import randint

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

    board.push(legalMoves[randint(0,len(legalMoves)-1)])

def otherPlayerMoves(board):
    move = raw_input()

    # If input is blank, just pick a random move
    if (move == ""):
        weMove(board)
        return

    move = chess.Move.from_uci(move)

    if (not(move in board.legal_moves)):
        print "Invalid move"
        otherPlayerMoves(board)
        return

    board.push(move)

def printBoard(board):
    print("###############")
    print(board)

def main(argv):
    color = 0

    if (argv[1] == "black"):
        color = chess.BLACK
    else:
        color = chess.WHITE

    board = chess.Board()

    printBoard(board)

    if (color == chess.BLACK): # other player goes first
        otherPlayerMoves(board)

    while (not(board.is_game_over())):
        printBoard(board)

        weMove(board)

        printBoard(board)
        print(evaluator.evaluate(board, chess.BLACK))

        otherPlayerMoves(board)


main(sys.argv)
