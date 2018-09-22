import logging
import itertools
import collections
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)



class Node:
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action

        if (self.parent == None):
            self.cost = 0
        else:
            self.cost = parent.cost + 1

    def __str__(self):
        return str(self.puzzle)

    @property
    def totalCH(self):
        return (self.cost + self.dist)

    @property
    def state(self):
        return str(self)

    @property
    def path(self):
        node = self
        tempPath = []
        while node:
            tempPath.append(node)
            node = node.parent
        yield from reversed(tempPath)

    @property
    def isSolved(self):
        return self.puzzle.isSolved

    @property
    def actions(self):
        return self.puzzle.actions

    @property
    def dist(self):
        return self.puzzle.manhattan


class Solver:
    def __init__(self, start):
        self.start = start

    def solve(self):
        queue = collections.deque([Node(self.start)])
        lSeen = set()
        lSeen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.totalCH))
            node = queue.popleft()

            if node.isSolved:
                return node.path

            for move, action in node.actions:
                c = Node(move(), node, action)

                if c.state not in lSeen:
                    queue.appendleft(c)
                    lSeen.add(c.state)

class Puzzle:
    def __init__(self, blocks):
        self.dimension = len(blocks[0])
        self.blocks = blocks

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.blocks:
            yield from row

    @property
    def isSolved(self):

        dimensions = self.dimension * self.dimension
        return str(self) == ''.join(map(str, range(1,dimensions))) + '0'

    @property
    def actions(self):
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.dimension),
                                      range(self.dimension)):
            direcs = {'right':(i, j-1),
                      'left':(i, j+1),
                      'down':(i-1, j),
                      'up':(i+1, j)}
            for action, (row, col) in direcs.items():
                if row >= 0 and col >= 0 and row < self.dimension and col < self.dimension and self.blocks[row][col] == 0:

                    if action == "right":
                        action = str(self.blocks[row][col+1])
                    elif action == "left":
                        action = str(self.blocks[row][col-1])
                    elif action == "down":
                        action = str(self.blocks[row+1][col])
                    else:
                        action = str(self.blocks[row-1][col])
                    move = create_move((i,j), (row,col)), action
                    moves.append(move)
        return moves

    @property
    def manhattan(self):
        distance = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.blocks[i][j] != 0:
                    x, y = divmod(self.blocks[i][j]-1, self.dimension)
                    distance += abs(x - i) + abs(y - j)
        return distance


    def copy(self):
        blocks = []
        for row in self.blocks:
            blocks.append([x for x in row])
        return Puzzle(blocks)

    def _move(self, at, to):
        puzzleCopy = self.copy()
        i, j = at
        r, c = to
        puzzleCopy.blocks[i][j], puzzleCopy.blocks[r][c] = puzzleCopy.blocks[r][c], puzzleCopy.blocks[i][j]
        return puzzleCopy


@app.route('/sorting-game', methods=['POST'])

def sorting():
    data = request.get_json()
    print("data sent for evaluation {}".format(data))

    result = []
    puzzle = data['puzzle']
    inputPuzzle = Puzzle(puzzle)
    s = Solver(inputPuzzle)
    solvePath = s.solve()
    for node in solvePath:
        if(node.action != None):
            result.append(int(node.action))

    print("My result :{}".format(result))
    return jsonify(result=result)
