import chess
from helpers import *
import evaluator

# We will only look this many moves ahead of the current board
# Must be multiple of 2
maxDepth = 4

# The tree that keeps track of moves
# Allocate starting with the board when its our player's turn
class MoveTree:
    def __init__(self, board):
        self.rootDepth = 0
        self.root = MoveNode(board, None, None, self, 0)
        self.color = board.turn

        self.root.findChildren()

    # Returns:
    # 0: The best move
    # 1: The index into children array where best move is found
    def evaluateTree(self):
        self.root.evaluate()

        m = -float("inf")
        index = 0
        for key,child in enumerate(self.root.children):
            if (child.value > m):
                m = child.value
                index = key

        return self.root.children[index].move

    # Chooses the move, updates tree root to that MoveNode
    def chooseMove(self, move):
        for child in self.root.children:
            if (child.move == move):
                self.rootDepth += 1
                self.root = child
                return

        print "Error: Move not found"
        quit()

    # Finds the next layer(s) of children
    def findNewChildren(self):
        self.root.findNewChildren()

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

    def findNewChildren(self):
        # We reached the leaves, no more children
        if (self.tree.rootDepth + maxDepth <= self.depth):
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

    def findChildren(self):
        # If our depth is maxDepth levels deeper than the root, we stop looking
        # at children.
        if (self.tree.rootDepth + maxDepth <= self.depth):
            return

        # Get all the legal moves
        legalMoves = getLegalMoves(self.board)

        self.children = []

        # Allocate new MoveNodes for each move, get their children too
        for move in legalMoves:
            nextBoard = self.board.copy()
            nextBoard.push(move)
            child = MoveNode(nextBoard, move, self, self.tree, self.depth+1)
            child.findChildren()
            self.children.append(child)

    def evaluate(self):
        if (self.depth%2 == 1):
            # Opponent is moving. We don't evaluate yet.
            return
        # If no children and we our analyzing our own move, evaluate this board.
        if ((self.children == None or len(self.children) == 0) and self.depth%2 == 0):
            val = evaluator.evaluate(self.board, self.tree.color)['material']
            self.value = val
            return

        childrenValues = []
        for child in self.children:
            child.evaluate()
            childrenValues.append(child.value)

        # If depth is odd, then we're on the opponents board.
        # Find the min value.
        if (self.depth%2 == 1):
            self.value = min(childrenValues)

        # If depth is even, then we're on our own board.
        # Find the max value.
        if (self.depth%2 == 0):
            self.value = max(childrenValues)

    def length(self, val):
        if (val == None):
            return 'None'
        else:
            return len(val)

    def printNode(self):
        if (self.move != None):
            print('--' * self.depth + ' move:' + str(self.move)+ ' children:' + str(self.length(self.children)))

        if (self.children == None):
            return

        for child in self.children:
            child.printNode()
