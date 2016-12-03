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
        self.maxDepth = 2

        self.root.findChildren()

    # Returns:
    # 0: The best move
    # 1: The index into children array where best move is found
    def evaluateTree(self):
        self.root.evaluate()

        countMax = 0
        m = -float("inf")
        index = 0
        for key,child in enumerate(self.root.children):
            if (child.value > m):
                countMax = 1
                m = child.value
                index = key
            elif (child.value == m):
                countMax += 1

        if (countMax == 1):
            return self.root.children[index].move
        else:
            select = randint(1, countMax)
            for key,child in enumerate(self.root.children):
                if (child.value != m):
                    continue
                if (select == 1):
                    print child.move
                    return child.move
                else:
                    select -= 1

        print self.root.children[index].move


    # Chooses the move, updates tree root to that MoveNode
    def chooseMove(self, move):
        if (self.maxDepth != 4 and getPieceCount(self.root.board) <= 13):
            self.maxDepth = 4
            self.findNewChildren()

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

    def findChildren(self):
        # If our depth is maxDepth levels deeper than the root, we stop looking
        # at children.
        if (self.tree.rootDepth + self.tree.maxDepth <= self.depth):
            return

        # Get all the legal moves
        legalMoves = getLegalMoves(self.board)

        self.children = []

        # Allocate new MoveNodes for each move, get their children too
        for move in legalMoves:
            nextBoard = self.board.copy(False)
            nextBoard.push(move)
            child = MoveNode(nextBoard, move, self, self.tree, self.depth+1)
            child.findChildren()
            self.children.append(child)

    # evaluate: Finds the value for a given node. Either finds the value of its
    #    children and computes its value, or runs the static evaluator function.
    def evaluate(self):
        # Odd depth means we moved to get to this board
        # Even depth means opponent moved to get to this board

        # If we're looking at their moves and there aren't any, it's an endgame
        if (self.depth%2 == 1 and (self.children == None or len(self.children) == 0)):
            self.value = getEndgameValue()
            return

        # If no children and we our analyzing our own move, evaluate this board.
        if (self.depth%2 == 0 and (self.children == None or len(self.children) == 0)):
            self.value = evaluator.evaluate(self.board, self.tree.color)
            return

        # Get all the values of the children
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

    # printNode: Prints the given node info and its children
    def printNode(self):
        if (self.move != None):
            print('--' * (self.depth-self.tree.rootDepth+1) + ' move:' + str(self.move)+ ' depth:' + str(self.depth) + ' score:' + str(self.value))
        if (self.children == None):
            return

        for child in self.children:
            child.printNode()
