import random
import math
import numpy
import threading
from multiprocessing import Pool, Lock

UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4

class Board():

    def __init__(self):
        self.won = False
        self.score = 0
        self.max = 2
        self.numMoves = 0
        self.empty = [(x, y) for x in range(4) for y in range(4)]
        self.cells = [[0]*4 for _ in range(4)]
        self.addTile()
        self.addTile()
        self.evaluation = 0
        self.lastmove = 0

    def __str__(self):
        """
        return a string representation of the current board.
        """
        rg = range(4)
        s = '\n'.join([' '.join([self.getCellStr(x, y) for x in rg]) for y in rg])
        return s + '\n' + str(self.evaluation) + '\n'

    def canMove(self):
        """
        return True if there are any possible moves, or False otherwise
        """
        if not self.filled():
            return True

        for y in xrange(0, 4):
            for x in xrange(0, 4):
                c = self.getCell(x, y)
                if (x < 3 and c == self.getCell(x+1, y)) or (y < 3 and c == self.getCell(x, y+1)):
                    return True

        return False

    def filled(self):
        """
        return True if the board is filled
        """
        return len(self.empty) == 0

    def addTile(self):
        """
        add a random tile in an empty cell
          choices: a list of possible choices for the value of the tile.
                   default is [2, 2, 2, 2, 2, 2, 2, 2, 2, 4].
        """
        v = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        if self.empty:
            x, y = random.choice(self.empty)
            self.setCell(x, y, v)
            self.getEmptyCells()

    def getCell(self, x, y):
        """return the cell value at x,y"""
        return self.cells[y][x]

    def getCellStr(self, x, y):
        """
        return a string representation of the cell located at x,y.
        """
        c = self.getCell(x, y)

        if c == 0:
            return '  .'
        elif c >= 1024:
            s = ' ' + str(int(2**(math.log(c, 2)-10))) + 'k'
        else:
            s = '%3d' % c

        return s

    def setCell(self, x, y, v):
        """set the cell value at x,y"""
        self.cells[y][x] = v

    def getLine(self, y):
        """return the y-th line, starting at 0"""
        return [self.getCell(i, y) for i in range(4)]

    def getCol(self, x):
        """return the x-th column, starting at 0"""
        return [self.getCell(x, i) for i in range(4)]

    def setLine(self, y, l):
        """set the y-th line, starting at 0"""
        for i in range(4):
            self.setCell(i, y, l[i])

    def setCol(self, x, l):
        """set the x-th column, starting at 0"""
        for i in range(4):
            self.setCell(x, i, l[i])

    def getEmptyCells(self):
        """return a (x, y) pair for each cell"""
        self.empty = [(x, y) for x in range(4) for y in range(4) if self.getCell(x, y) == 0]

    def __collapseLineOrCol(self, line, d):
        """
        Merge tiles in a line or column according to a direction and return a
        tuple with the new line and the score for the move on this line
        """
        if (d == LEFT or d == UP):
            inc = 1
            rg = xrange(0, 3, inc)
        else:
            inc = -1
            rg = xrange(3, 0, inc)

        pts = 0
        for i in rg:
            if line[i] == 0:
                continue
            if line[i] == line[i+inc]:
                v = line[i]*2
                if v == 2048:
                    self.won = True

                line[i] = v
                line[i+inc] = 0
                pts += v

        return (line, pts)

    def __moveLineOrCol(self, line, d):
        """
        Move a line or column to a given direction (d)
        """
        nl = [c for c in line if c != 0]
        if d == UP or d == LEFT:
            return nl + [0] * (4 - len(nl))
        return [0] * (4 - len(nl)) + nl

    def move(self, d, add_tile=True):
        """
        move and return the move score
        """
        if d == LEFT or d == RIGHT:
            chg, get = self.setLine, self.getLine
        elif d == UP or d == DOWN:
            chg, get = self.setCol, self.getCol
        else:
            return 0

        moved = False
        tempscore = 0

        for i in range(4):
            origin = get(i)
            line = self.__moveLineOrCol(origin, d)
            collapsed, pts = self.__collapseLineOrCol(line, d)
            new = self.__moveLineOrCol(collapsed, d)
            chg(i, new)
            if origin != new:
                moved = True
            tempscore += pts

        self.getEmptyCells()
        for i in range(4):
            for j in range(4):
                if self.cells[i][j] > self.max:
                    self.max == self.cells[i][j]

        if moved and add_tile:
            self.addTile()

        self.score += tempscore
        self.numMoves += 1

        return moved


def possibleNewTiles(board):
    result_twos = []
    result_fours = []
    for cell in board.empty:
        newboard = Board()
        newboard.max = board.max
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.setCell(cell[0], cell[1], 2)
        #evaluate(newboard)
        result_twos.append(newboard)
        newboard = Board()
        newboard.max = board.max
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.setCell(cell[0], cell[1], 4)
        #evaluate(newboard)
        result_fours.append(newboard)

    return result_twos, result_fours


def generateDepthOne(board, available):
    result = []
    for i in available:
        newboard = Board()
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.move(i, False)
        newboard.lastmove = i
        result.append(newboard)
    return result


def availableMoves(board):
    moves = []
    newboard = Board()
    for i in range(1, 5):
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        if newboard.move(i):
            moves.append(i)
    return moves

def evaluateOneBoard(board):
    evaluate(board)
    print board

def evaluate(board, free=2, punishment=2):
    result = 0
    for i in range(4):
        for j in range(3):
            result += math.fabs(board.cells[j][i] - board.cells[j+1][i]) * 1.1
            result += math.fabs(board.cells[i][j] - board.cells[i][j+1]) * 1.1
            if board.cells[i][j] == board.cells[i][j+1]:
                result -= board.cells[i][j] * 1.76
            if board.cells[j][i] == board.cells[j+1][i]:
                result -= board.cells[j][i] * 1.76
    try:
        result /= len(board.empty)
    except:
        pass
    result -= board.max
    board.evaluation = result
    return result


# def soHeuristic(board):
#     result = 0
#     for x in range(4):
#         if board.cells[x][0] >= board.cells[x][1] >= board.cells[x][2] >= board.cells[x][3]:
#             result += max(board.cells[x][0], board.cells[x][1], board.cells[x][2], board.cells[x][3])
#         if board.cells[0][x] >= board.cells[1][x] >= board.cells[2][x] >= board.cells[3][x]:
#             result += max(board.cells[0][x], board.cells[1][x], board.cells[2][x], board.cells[3][x])
#         if board.cells[x][0] <= board.cells[x][1] <= board.cells[x][2] <= board.cells[x][3]:
#             result += max(board.cells[x][0], board.cells[x][1], board.cells[x][2], board.cells[x][3])
#         if board.cells[0][x] <= board.cells[1][x] <= board.cells[2][x] <= board.cells[3][x]:
#             result += max(board.cells[0][x], board.cells[1][x], board.cells[2][x], board.cells[3][x])
#         for y in range(3):
#             if board.cells[x][y] == board.cells[x][y+1]:
#                 result += board.cells[x][y] * 2
#             if board.cells[y][x] == board.cells[y+1][x]:
#                 result += board.cells[y][x] * 2
#     result *= len(board.empty)
#     return result


def AIRandomAvailableMove(board, available):
    return random.choice(available)


def AIPreferenceMove(board, available):
    if 4 in available:
        return 4
    if 1 in available:
        return 1
    if 3 in available:
        return 3
    if 2 in available:
        return 2


def AIHighScoreMove(board, available):
    move = 0
    best = -1
    newboard = Board()
    newboard.score = board.score
    for i in available:
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.move(i)
        if newboard.score > best:
            best = newboard.score
            move = i
    return move


def AIFreeSpaceMove(board, available):
    move = 0
    best = -1
    newboard = Board()
    newboard.empty = board.empty
    for i in available:
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.move(i)
        if len(newboard.empty) > best:
            best = len(newboard.empty)
            move = i
    return move


def AISmoothBoard(board, available):
    move = 0
    best = float("inf")
    newboard = Board()
    newboard.max = board.max
    for i in available:
        for x in range(4):
            for y in range(4):
                newboard.cells[x][y] = board.cells[x][y]
        newboard.move(i, False)
        evaluate(newboard)
        if newboard.evaluation < best:
            best = newboard.evaluation
            move = i
    return move, best


def AISmoothDepthOne(board, available):
    best = 999999
    result = [[],[],[],[]]
    result2 = [0,0,0,0]
    boards = generateDepthOne(board, available)
    for b in boards:
        b.getEmptyCells()
        result2[b.lastmove-1] = evaluate(b)
        newboards2, newboards4 = possibleNewTiles(b)
        for newboard in newboards2:
            newboard.getEmptyCells()
            evaluate(newboard)
            result[b.lastmove-1].append(newboard.evaluation * .9)
        for newboard in newboards4:
            newboard.getEmptyCells()
            evaluate(newboard)
            result[b.lastmove-1].append(newboard.evaluation * .1)
    for i in range(len(result)):
        try:
            result[i] = (sum(result[i])/len(result[i]) * 1) + (result2[i])
        except ZeroDivisionError:
            result[i] = 0
    for i in range(len(result)):
        if result[i] == 0:
            result[i] = 999999
        if result[i] < best:
            best = result[i]
            move = i+1
    return move, best



def AITest(rounds=200):
    scores = []
    moves = []
    best = 0
    worst = 999999
    bestboard = []
    worstboard = []
    wins = 0
    for _ in range(rounds):
        a = Board()
        available = availableMoves(a)
        while available:
            movetomake, evaluation = AISmoothDepthOne(a, available)
            a.evaluation = evaluation
            a.move(movetomake)
            available = availableMoves(a)
        if a.won:
            wins += 1
        if a.score > best:
            best = a.score
            bestboard = a
        if a.score < worst:
            worst = a.score
            worstboard = a
        scores.append(a.score)
        moves.append(a.numMoves)

    avgscore = sum(scores)/float(len(scores))
    avgmoves = sum(moves)/float(len(moves))
    winpercent = float(wins)/float(rounds)*100
    return [avgscore, scores, avgmoves, wins, winpercent, bestboard, worstboard, best, worst]
    scores = []
    moves = []
    wins = 0
    best = 0
    worst = 999999

if __name__ == '__main__':
    avgscore = []
    stdscore = []
    scoreslist = []
    avgmoves = []
    wins  = []
    winpercent = []
    bestboard = 0
    worstboard = 0
    best = 0
    worst = 999999
    x = [20]*50
    pool = Pool(7)
    results = pool.map(AITest, x)
    for result in results:
        avgscore.append(result[0])
        scoreslist.append(result[1])
        avgmoves.append(result[2])
        wins.append(result[3])
        winpercent.append(result[4])
        if result[7] > best:
            best = result[7]
            bestboard = result[5]
        if result[8] < worst:
            worst = result[8]
            worstboard = result[6]
    for score in scoreslist:
        stdscore.append(score)
    stdscore = numpy.std(stdscore)

    print 'average score: ' + str(sum(avgscore)/float(len(avgscore)))
    print 'score stdev: ' + str(stdscore)
    print 'average moves: ' + str(sum(avgmoves)/float(len(avgmoves)))
    print 'wins: ' + str(sum(wins))
    print 'win percentage: ' + str(sum(winpercent)/float(len(winpercent))) + '%'
    print 'best score: ' + str(best)
    print bestboard
    print 'worst score: ' + str(worst)
    print worstboard
    print '\n'