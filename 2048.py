import random
import cProfile

left = 0
right = 1
up = 2
down = 3


def NewTile():
	return random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])


def NewPos(available):
	return random.choice(available)


class Board():
	def __init__(self):
		self.board = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
		self.count = 0
		self.score = 0

		while self.count < 2:
			available = []
			for i in range(0,4):
				for j in range(0,4):
					if self.board[i][j] is None:
						available.append([i,j])
			pos = NewPos(available)
			self.board[pos[0]][pos[1]] = NewTile()
			self.count += 1


	def __str__(self):
		string = ''
		for row in self.board:
			for j in row:
				if j is None:
					string = string + 'x '
				else:
					string = string + str(j) + ' '
			string = string + '\n'
		string = string + 'score: ' + str(self.score) + '\n'
		return string


	def __repr__(self):
		return str(self.board)


def moveLeft(board):
	newboard = Board()
	for i in range(0,4):
		for j in range(0,4):
			newboard.board[i][j] = board.board[i][j]
	newboard.score = board.score
	for i in range(0, 4):
		temp = []
		for j in range(0, 4):
			if newboard.board[i][j] is not None:
				temp.append(newboard.board[i][j])
		while len(temp) < 4:
			temp.append(None)
		newboard.board[i] = temp
		if newboard.board[i][0] == newboard.board[i][1] and newboard.board[i][2] == newboard.board[i][3] and newboard.board[i][0] is not None and newboard.board[i][2] is not None:
			newboard.board[i][0] = newboard.board[i][0] * 2
			newboard.board[i][1] = newboard.board[i][1] * 2
			newboard.board[i][2] = None
			newboard.board[i][3] = None
			newboard.score = newboard.score + newboard.board[i][0]
			newboard.score = newboard.score + newboard.board[i][1]
		elif newboard.board[i][0] == newboard.board[i][1] and newboard.board[i][0] is not None:
			newboard.board[i][0] = newboard.board[i][0] * 2
			newboard.board[i][1] = newboard.board[i][2]
			newboard.board[i][2] = newboard.board[i][3]
			newboard.board[i][3] = None
			newboard.score = newboard.score + newboard.board[i][0]
		elif newboard.board[i][1] == newboard.board[i][2] and newboard.board[i][1] is not None:
			newboard.board[i][1] = newboard.board[i][1] * 2
			newboard.board[i][2] = newboard.board[i][3]
			newboard.board[i][3] = None
			newboard.score = newboard.score + newboard.board[i][1]
		elif newboard.board[i][2] == newboard.board[i][3] and newboard.board[i][2] is not None:
			newboard.board[i][2] = newboard.board[i][2] * 2
			newboard.board[i][3] = None
			newboard.score = newboard.score + newboard.board[i][2]
	return newboard


def moveRight(board):
	newboard = Board()
	for i in range(0,4):
		for j in range(0,4):
			newboard.board[i][j] = board.board[i][j]
	newboard.score = board.score
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if newboard.board[i][j] is not None:
				temp.append(newboard.board[i][j])
		while len(temp) < 4:
			temp.insert(0, None)
		newboard.board[i] = temp
		if newboard.board[i][0] == newboard.board[i][1] and newboard.board[i][2] == newboard.board[i][3] and newboard.board[i][0] is not None and newboard.board[i][2] is not None:
			newboard.board[i][3] = newboard.board[i][2] * 2
			newboard.board[i][2] = newboard.board[i][1] * 2
			newboard.board[i][0] = None
			newboard.board[i][1] = None
			newboard.score = newboard.score + newboard.board[i][3]
			newboard.score = newboard.score + newboard.board[i][2]
		elif newboard.board[i][2] == newboard.board[i][3] and newboard.board[i][2] is not None:
			newboard.board[i][3] = newboard.board[i][2] * 2
			newboard.board[i][2] = newboard.board[i][1]
			newboard.board[i][1] = newboard.board[i][0]
			newboard.board[i][0] = None
			newboard.score = newboard.score + newboard.board[i][3]
		elif newboard.board[i][1] == newboard.board[i][2] and newboard.board[i][1] is not None:
			newboard.board[i][2] = newboard.board[i][1] * 2
			newboard.board[i][1] = newboard.board[i][0]
			newboard.board[i][0] = None
			newboard.score = newboard.score + newboard.board[i][2]
		elif newboard.board[i][0] == newboard.board[i][1] and newboard.board[i][0] is not None:
			newboard.board[i][1] = newboard.board[i][0] * 2
			newboard.board[i][0] = None
			newboard.score = newboard.score + newboard.board[i][1]
	return newboard


def moveUp(board):
	newboard = Board()
	for i in range(0,4):
		for j in range(0,4):
			newboard.board[i][j] = board.board[i][j]
	newboard.score = board.score
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if newboard.board[j][i] is not None:
				temp.append(newboard.board[j][i])
		while len(temp) < 4:
			temp.append(None)
		for j in range(0,4):
			newboard.board[j][i] = temp[j]
		if newboard.board[0][i] == newboard.board[1][i] and newboard.board[2][i] == newboard.board[3][i] and newboard.board[0][i] is not None and newboard.board[2][i] is not None:
			newboard.board[0][i] = newboard.board[0][i] * 2
			newboard.board[1][i] = newboard.board[1][i] * 2
			newboard.board[2][i] = None
			newboard.board[3][i] = None
			newboard.score = newboard.score + newboard.board[0][i]
			newboard.score = newboard.score + newboard.board[1][i]
		elif newboard.board[0][i] == newboard.board[1][i] and newboard.board[0][i] is not None:
			newboard.board[0][i] = newboard.board[0][i] * 2
			newboard.board[1][i] = newboard.board[2][i]
			newboard.board[2][i] = newboard.board[3][i]
			newboard.board[3][i] = None
			newboard.score = newboard.score + newboard.board[0][i]
		elif newboard.board[1][i] == newboard.board[2][i] and newboard.board[1][i] is not None:
			newboard.board[1][i] = newboard.board[2][i] * 2
			newboard.board[2][i] = newboard.board[3][i]
			newboard.board[3][i] = None
			newboard.score = newboard.score + newboard.board[1][i]
		elif newboard.board[2][i] == newboard.board[3][i] and newboard.board[2][i] is not None:
			newboard.board[2][i] = newboard.board[2][i] * 2
			newboard.board[3][i] = None
			newboard.score = newboard.score + newboard.board[2][i]
	return newboard


def moveDown(board):
	newboard = Board()
	for i in range(0,4):
		for j in range(0,4):
			newboard.board[i][j] = board.board[i][j]
	newboard.score = board.score
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if newboard.board[j][i] is not None:
				temp.append(newboard.board[j][i])
		while len(temp) < 4:
			temp.insert(0, None)
		for j in range(0,4):
			newboard.board[j][i] = temp[j]
		if newboard.board[0][i] == newboard.board[1][i] and newboard.board[2][i] == newboard.board[3][i] and newboard.board[0][i] is not None and newboard.board[2][i] is not None:
			newboard.board[3][i] = newboard.board[2][i] * 2
			newboard.board[2][i] = newboard.board[1][i] * 2
			newboard.board[0][i] = None
			newboard.board[1][i] = None
			newboard.score = newboard.score + newboard.board[3][i]
			newboard.score = newboard.score + newboard.board[2][i]
		elif newboard.board[2][i] == newboard.board[3][i] and newboard.board[2][i] is not None:
			newboard.board[3][i] = newboard.board[2][i] * 2
			newboard.board[2][i] = newboard.board[1][i]
			newboard.board[1][i] = newboard.board[0][i]
			newboard.board[0][i] = None
			newboard.score = newboard.score + newboard.board[3][i]
		elif newboard.board[1][i] == newboard.board[2][i] and newboard.board[1][i] is not None:
			newboard.board[2][i] = newboard.board[1][i] * 2
			newboard.board[1][i] = newboard.board[0][i]
			newboard.board[0][i] = None
			newboard.score = newboard.score + newboard.board[2][i]
		elif newboard.board[0][i] == newboard.board[1][i] and newboard.board[0][i] is not None:
			newboard.board[1][i] = newboard.board[0][i] * 2
			newboard.board[0][i] = None
			newboard.score = newboard.score + newboard.board[1][i]
	return newboard


def addPiece(board):
	available = []
	for i in range(0,4):
		for j in range(0,4):
			if board.board[i][j] is None:
				available.append([i,j])
	try:
		pos = NewPos(available)
		board.board[pos[0]][pos[1]] = NewTile()
	except IndexError:
		pass


def move(direction, board):
	newboard = Board()
	newboard.board = board.board
	if direction == left:
		newboard = moveLeft(board)
	elif direction == right:
		newboard = moveRight(board)
	elif direction == up:
		newboard = moveUp(board)
	elif direction == down:
		newboard = moveDown(board)
	else:
		return 'UNKNOWN MOVE'
	addPiece(newboard)
	return newboard


def availableMoves(board):
	available = []
	newboard = Board()
	for i in range(0,4):
		for j in range(0,4):
			newboard.board[i][j] = board.board[i][j]
	if newboard.board != moveLeft(newboard).board:
		available.append(left)
	if newboard.board != moveRight(newboard).board:
		available.append(right)
	if newboard.board != moveUp(newboard).board:
		available.append(up)
	if newboard.board != moveDown(newboard).board:
		available.append(down)
	if not available:
		return None
	else:
		return available


def play():
	a = Board()
	while availableMoves(a) is not None:
		print a
		s = raw_input()
		if s.lower() == 'left':
			print move(left, a)
		if s.lower() == 'right':
			print move(right, a)
		if s.lower() == 'up':
			print move(up, a)
		if s.lower() == 'down':
			print move(down, a)

def AIRandomAvailableMove():
	numMoves = 0
	a = Board()
	available = availableMoves(a)
	while available is not None:
		#print available
		#print a
		a = move(random.choice(available), a)
		available = availableMoves(a)
		numMoves = numMoves + 1
	#print available
	#print a
	return a.score, numMoves

score = []
moves = []
for i in range(0,1000):
	result = AIRandomAvailableMove()
	score.append(result[0])
	moves.append(result[1])

print sum(score)/float(len(score))
print sum(moves)/float(len(moves))