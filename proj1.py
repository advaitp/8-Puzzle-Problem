import numpy as np
import time

def findZero(board) :
	for i in range(3) :
		for j in range(3) :
			if board[i][j] == 0 :
				return i, j
	return -1, -1

def checkLeft(x, y, board) :
	w, h = board.shape
	move = False
	if y-1 >= 0:
		move = True
	return move

def checkRight(x, y, board) :
	w, h = board.shape
	move = False
	if y+1 < w:
		move = True
	return move

def checkUp(x, y, board) :
	w, h = board.shape
	move = False
	if x-1 >= 0:
		move = True
	return move

def checkDown(x, y, board) :
	w, h = board.shape
	move = False
	if x+1 < h:
		move = True
	return move

def checkBoard(board1, board2) :
	return (board1==board2).all()

def findNeigh(x0, y0, board):
	ne = []
	lm = checkLeft(x0, y0, board)
	rm = checkRight(x0, y0, board)
	um = checkUp(x0, y0, board)
	dm = checkDown(x0, y0, board)
	
	if lm : ne.append([x0, y0-1])
	if um : ne.append([x0-1, y0])
	if rm : ne.append([x0, y0+1])
	if dm : ne.append([x0+1, y0])
		
	return ne

def traverse(xi, yi, xf, yf, board) :
	cboard = board.copy()
	cboard[xi][yi], cboard[xf][yf] = cboard[xf][yf], cboard[xi][yi]
	return cboard

def printBoard(cboard, iteration) :
	print(f'-----------Printing New Board for iteration {iteration}-----------')
	for i in range(3) :
		for j in range(3) :
			print(cboard[i][j],end="|")
		print()
		print('---------------')
	print()

def statePresent(cboard, states) :
	present = False
	for state in states:
		if checkBoard(cboard, state) : present = True

	return present

def generatePath(xi, yi, board, fboard):
	states = []
	queue = []
	paths = []
	pc = {}
	iterations = 1
	queue.append([xi, yi, board, iterations])
	flag = True
	cboard = np.full((3, 3), -1)
	paths.append(board.T)
	pc[1] = 0

	while queue and flag:
		px, py, pboard, pidx = queue.pop(0)
		children = findNeigh(px, py, pboard)
		states.append(pboard)
		for (x,y) in children:
			cboard = traverse(px, py, x, y, pboard)
			if not statePresent(cboard, states) :
				iterations += 1
				pc[iterations] = pidx
				queue.append([x,y,cboard, iterations])
				states.append(cboard)
				paths.append(cboard.T)

				if checkBoard(cboard, fboard) :
					flag = False
					break

	return paths, pc

def cvtPathtostring(path) : 
	pstr = ''
	r, c = path.shape[0], path.shape[1]
	for i in range(r) :
		for j in range(c) :
			pstr += str(path[i][j]) + ' '

	return pstr

def pathTotxt(paths, bpaths) :
	with open("Nodes.txt", "w") as file:
		for path in paths : 
			pstr = cvtPathtostring(path)
			file.write(f"{pstr}\n")

	with open("nodePath.txt", "w") as file:
		for path in bpaths : 
			pstr = cvtPathtostring(path)
			file.write(f"{pstr}\n")

def getInvcount(board) :
	invc = 0 
	nums = board.flatten()
	for i in range(nums.shape[0]-1) :
		for j in range(i + 1, nums.shape[0]):
			if nums[j] != 0 and nums[i] != 0 and nums[i] > nums[j]:
				invc += 1
	return invc

def checkSolve(board) :
	inv = getInvcount(board)
	return inv % 2 == 0 

def nodesInfo(parChild) :
	with open("NodesInfo.txt", "w") as file:
		file.write(f"Node_index   Parent_Node_index   Cost\n")
		for child in parChild : 
			file.write(f"{child}  {parChild[child]}  {0}\n")

if __name__ == "__main__" :
	stime = time.time()
	r, c = 3, 3
	board = np.array([[2,8,3],[1,6,4],[7,0,5]])
	fboard = np.array([[1,2,3],[8,0,4],[7,6,5]])

	iteration = 1
	bpaths = []
	x0, y0 = findZero(board)
	paths, parChild = generatePath(x0, y0, board, fboard)
	count = 2

	fidx = len(paths)
	indexes = []
	bpaths.append(fboard.T)
	while parChild[fidx] != 1 :
		indexes.append(parChild[fidx])
		bpaths.append(paths[parChild[fidx]-1])
		fidx = parChild[fidx]

	bpaths.append(board.T)
	bpaths.reverse()
	pathTotxt(paths, bpaths)
	nodesInfo(parChild)
	etime = time.time()
	print(f'Time taken for executon : {etime-stime}')
