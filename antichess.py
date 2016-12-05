import chess
import sys
import evaluator
from random import randint
from helpers import *
from tree import *
import time

def aiMove(board):
    moveTree = MoveTree(board)
    #moveTree.printTree()
    bestMove = moveTree.getBestMove()

    print str(bestMove[0])
    board.push(bestMove[0])

def randomMove(board):
    legalMoves = getLegalMoves(board)
    return legalMoves[randint(0, len(legalMoves)-1)]

def inputMove(board):
    print 'Input move:'
    move = raw_input()

    # If input is blank, just pick a random move
    if (move == ""):
        move = randomMove(board)
    else:
        move = chess.Move.from_uci(move)

    if (not(move in getLegalMoves(board))):
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

    # Other player goes first
    if (color == chess.BLACK):
        printBoard(board)
        inputMove(board)

    while (True):
        printBoard(board)
        aiMove(board)

        if (board.is_game_over()):
            print board.result()
            break

        printBoard(board)
        inputMove(board)

        if (board.is_game_over()):
            print board.result()
            break

main(sys.argv)
