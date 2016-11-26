import chess
import sys
import evaluator
from random import randint
from helpers import *

def aiMove(board):
    legalMoves = getLegalMoves(board)
    board.push(legalMoves[randint(0,len(legalMoves)-1)])

def randomMove(board):
    legalMoves = getLegalMoves(board)
    board.push(legalMoves[randint(0,len(legalMoves)-1)])

def inputMove(board):
    move = raw_input()

    # If input is blank, just pick a random move
    if (move == ""):
        randomMove(board)
        return

    move = chess.Move.from_uci(move)

    if (not(move in board.legal_moves)):
        print "Invalid move"
        inputMove(board)
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
        inputMove(board)

    while (not(board.is_game_over())):
        printBoard(board)
        print(evaluator.evaluate(board, chess.BLACK))

        aiMove(board)

        printBoard(board)

        inputMove(board)


main(sys.argv)
