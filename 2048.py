import random

left = 0
right = 1
up = 2
down = 3


def NewTile():
	return random.choice([2,4])


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
	for i in range(0, 4):
		temp = []
		for j in range(0, 4):
			if board.board[i][j] is not None:
				temp.append(board.board[i][j])
		while len(temp) < 4:
			temp.append(None)
		board.board[i] = temp
		if board.board[i][0] == board.board[i][1] and board.board[i][2] == board.board[i][3] and board.board[i][0] is not None and board.board[i][2] is not None:
			board.board[i][0] = board.board[i][0] * 2
			board.board[i][1] = board.board[i][1] * 2
			board.board[i][2] = None
			board.board[i][3] = None
			board.score = board.score + board.board[i][0]
			board.score = board.score + board.board[i][1]
		elif board.board[i][0] == board.board[i][1] and board.board[i][0] is not None:
			board.board[i][0] = board.board[i][0] * 2
			board.board[i][1] = board.board[i][2]
			board.board[i][2] = board.board[i][3]
			board.board[i][3] = None
			board.score = board.score + board.board[i][0]
		elif board.board[i][1] == board.board[i][2] and board.board[i][1] is not None:
			board.board[i][1] = board.board[i][1] * 2
			board.board[i][2] = board.board[i][3]
			board.board[i][3] = None
			board.score = board.score + board.board[i][1]
		elif board.board[i][2] == board.board[i][3] and board.board[i][2] is not None:
			board.board[i][2] = board.board[i][2] * 2
			board.board[i][3] = None
			board.score = board.score + board.board[i][2]
	return board


def moveRight(board):
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if board.board[i][j] is not None:
				temp.append(board.board[i][j])
		while len(temp) < 4:
			temp.insert(0, None)
		board.board[i] = temp
		if board.board[i][0] == board.board[i][1] and board.board[i][2] == board.board[i][3] and board.board[i][0] is not None and board.board[i][2] is not None:
			board.board[i][3] = board.board[i][2] * 2
			board.board[i][2] = board.board[i][1] * 2
			board.board[i][0] = None
			board.board[i][1] = None
			board.score = board.score + board.board[i][3]
			board.score = board.score + board.board[i][2]
		elif board.board[i][2] == board.board[i][3] and board.board[i][2] is not None:
			board.board[i][3] = board.board[i][2] * 2
			board.board[i][2] = board.board[i][1]
			board.board[i][1] = board.board[i][0]
			board.board[i][0] = None
			board.score = board.score + board.board[i][3]
		elif board.board[i][1] == board.board[i][2] and board.board[i][1] is not None:
			board.board[i][2] = board.board[i][1] * 2
			board.board[i][1] = board.board[i][0]
			board.board[i][0] = None
			board.score = board.score + board.board[i][2]
		elif board.board[i][0] == board.board[i][1] and board.board[i][0] is not None:
			board.board[i][1] = board.board[i][0] * 2
			board.board[i][0] = None
			board.score = board.score + board.board[i][1]
	return board


def moveUp(board):
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if board.board[j][i] is not None:
				temp.append(board.board[j][i])
		while len(temp) < 4:
			temp.append(None)
		for j in range(0,4):
			board.board[j][i] = temp[j]
		if board.board[0][i] == board.board[1][i] and board.board[2][i] == board.board[3][i] and board.board[0][i] is not None and board.board[2][i] is not None:
			board.board[0][i] = board.board[0][i] * 2
			board.board[1][i] = board.board[1][i] * 2
			board.board[2][i] = None
			board.board[3][i] = None
			board.score = board.score + board.board[0][i]
			board.score = board.score + board.board[1][i]
		elif board.board[0][i] == board.board[1][i] and board.board[0][i] is not None:
			board.board[0][i] = board.board[0][i] * 2
			board.board[1][i] = board.board[2][i]
			board.board[2][i] = board.board[3][i]
			board.board[3][i] = None
			board.score = board.score + board.board[0][i]
		elif board.board[1][i] == board.board[2][i] and board.board[1][i] is not None:
			board.board[1][i] = board.board[2][i] * 2
			board.board[2][i] = board.board[3][i]
			board.board[3][i] = None
			board.score = board.score + board.board[1][i]
		elif board.board[2][i] == board.board[3][i] and board.board[2][i] is not None:
			board.board[2][i] = board.board[2][i] * 2
			board.board[3][i] = None
			board.score = board.score + board.board[2][i]
	return board


def moveDown(board):
	for i in range(0,4):
		temp = []
		for j in range(0,4):
			if board.board[j][i] is not None:
				temp.append(board.board[j][i])
		while len(temp) < 4:
			temp.insert(0, None)
		for j in range(0,4):
			board.board[j][i] = temp[j]
		if board.board[0][i] == board.board[1][i] and board.board[2][i] == board.board[3][i] and board.board[0][i] is not None and board.board[2][i] is not None:
			board.board[3][i] = board.board[2][i] * 2
			board.board[2][i] = board.board[1][i] * 2
			board.board[0][i] = None
			board.board[1][i] = None
			board.score = board.score + board.board[3][i]
			board.score = board.score + board.board[2][i]
		elif board.board[2][i] == board.board[3][i] and board.board[2][i] is not None:
			board.board[3][i] = board.board[2][i] * 2
			board.board[2][i] = board.board[1][i]
			board.board[1][i] = board.board[0][i]
			board.board[0][i] = None
			board.score = board.score + board.board[3][i]
		elif board.board[1][i] == board.board[2][i] and board.board[1][i] is not None:
			board.board[2][i] = board.board[1][i] * 2
			board.board[1][i] = board.board[0][i]
			board.board[0][i] = None
			board.score = board.score + board.board[2][i]
		elif board.board[0][i] == board.board[1][i] and board.board[0][i] is not None:
			board.board[1][i] = board.board[0][i] * 2
			board.board[0][i] = None
			board.score = board.score + board.board[1][i]
	return board


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
	if direction == left:
		board = moveLeft(board)
	elif direction == right:
		board = moveRight(board)
	elif direction == up:
		board = moveUp(board)
	elif direction == down:
		board = moveDown(board)
	else:
		return 'UNKNOWN MOVE'
	addPiece(board)
	return board


a = Board()
print a
for i in range(0,1000):
	move(random.choice([0,1,2]), a)
print a


def play():
	a = Board()
	while True:
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
