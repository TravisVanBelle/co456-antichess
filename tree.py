import chess
from helpers import *
from random import randint
import evaluator


# The tree that keeps track of moves
# Allocate starting with the board when its our player's turn
class MoveTree:
    def __init__(self, board):
        self.rootDepth = 0
        self.root = MoveNode(board, None, None, self, 0)
        self.color = board.turn

        # We will only look this many moves ahead of the current board
        # Must be multiple of 2
        self.maxDepth = 4

        # Gets the tree
        self.getTree()

    def getTree(self):
        self.root.getTree(-float("inf"), float("inf"))

    # Returns the best move
    def getBestMove(self):
        maxMoves = []
        m = -float("inf")

        index = 0
        for key,child in enumerate(self.root.children):
            if (child.value > m):
                maxMoves = [child]
                m = child.value
                index = key
            elif (child.value == m):
                maxMoves.append(child)

        select = randint(0, len(maxMoves)-1)

        return (maxMoves[select].move, maxMoves[select].value)


    # Displays the tree
    def printTree(self):
        self.root.printNode()

# board: The board that results from the move
# move: The move played to get to the current board
# parent: The board that existed before the move
# tree: The MoveTree object
# depth: The depth of the current move node
class MoveNode:
    def __init__(self, board, move, parent, tree, depth):
        self.board = board
        self.move = move
        self.parent = parent
        self.tree = tree
        self.children = None
        self.depth = depth
        self.value = None

    # Gets the tree and evaluation. Prunes on the way.
    # Returns tuple (alpha, beta), numbers or None.
    def getTree(self, alpha, beta):
        # We reached max depth of the tree
        if (self.tree.rootDepth + self.tree.maxDepth <= self.depth):
            self.value = evaluator.evaluate(self.board, self.tree.color)
            return

        # Depth is odd, at a min node
        if (self.depth%2 == 1):
            legalMoves = getLegalMoves(self.board)

            self.children = []

            m = float("inf")

            if (len(legalMoves) == 0):
                self.value = getEndgameValue()
                return

            for move in legalMoves:
                nextBoard = self.board.copy(False)
                nextBoard.push(move)
                child = MoveNode(nextBoard, move, self, self.tree, self.depth+1)
                child.getTree(alpha, beta)

                if (child.value < beta):
                    beta = child.value

                if (child.value < m):
                    m = child.value

                self.children.append(child)

                if (beta <= alpha):
                    self.value = m-1
                    return

            self.value = m-1

        # Depth is even, at a max node
        if (self.depth%2 == 0):
            legalMoves = getLegalMoves(self.board)
            self.children = []

            m = -float("inf")

            if (len(legalMoves) == 0):
                self.value = -getEndgameValue()
                return

            for move in legalMoves:
                nextBoard = self.board.copy(False)
                nextBoard.push(move)
                child = MoveNode(nextBoard, move, self, self.tree, self.depth+1)
                child.getTree(alpha, beta)

                if (child.value > alpha):
                    alpha = child.value

                if (child.value > m):
                    m = child.value

                self.children.append(child)

                if (beta <= alpha):
                    self.value = m-1
                    return

            self.value = m-1

    def findNewChildren(self):
        # We reached the leaves, no more children
        if (self.tree.rootDepth + self.tree.maxDepth <= self.depth):
            return

        # The current node hasn't found any children, so it must have been just
        # initialized.
        if (self.children == None):
            self.findChildren()
        # Current node has children. Keep em, and find all the new children of
        # the current node's children.
        else:
            for children in self.children:
                children.findNewChildren()

    # printNode: Prints the given node info and its children
    def printNode(self):
        if (self.move != None):
            print('--' * (self.depth-self.tree.rootDepth+1) + ' move:' + str(self.move)+ ' depth:' + str(self.depth) + ' score:' + str(self.value))
        if (self.children == None):
            return

        for child in self.children:
            child.printNode()
