import chess
import sys
import evaluator
from random import randint
from helpers import *
from tree import *

def aiMove(board, moveTree):
    bestMove = moveTree.evaluateTree()
    board.push(bestMove)

    moveTree.chooseMove(bestMove)

def randomMove(board):
    legalMoves = getLegalMoves(board)
    return legalMoves[randint(0, len(legalMoves)-1)]

def inputMove(board, moveTree = False):
    print 'Input move:'
    move = raw_input()

    # If input is blank, just pick a random move
    if (move == ""):
        move = randomMove(board)
    else:
        move = chess.Move.from_uci(move)

    if (not(move in board.legal_moves)):
        print "Invalid move"
        inputMove(board)
        return

    board.push(move)

    if (moveTree):
        moveTree.chooseMove(move)
        moveTree.findNewChildren()

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

    moveTree = MoveTree(board)

    while (not(board.is_game_over())):
        printBoard(board)
        aiMove(board, moveTree)

        printBoard(board)
        inputMove(board, moveTree)




main(sys.argv)
