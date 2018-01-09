import numpy as np 
import pyautogui as pui
import mss
import mss.tools
from PIL import Image

width = 16
height = 16 
undiscovered = np.zeros((width, height), dtype=int)
board =  np.full((width, height), fill_value=9, dtype=int)
offset = 7
screenRegion = {'top': 0, 'left': 0, 'width': pui.size()[0], 'height': pui.size()[1]}

def locate_playing_field():
	right, top = pui.locateCenterOnScreen('images/topRightCorner.png')
	left, bot = pui.locateCenterOnScreen('images/botLeftCorner.png')
	return (left//2+offset, right//2-offset, top//2+offset, bot//2-offset)

def start_game():
	smiley = pui.locateCenterOnScreen('images/smiley.png')
	if smiley is None:
		smiley = pui.locateCenterOnScreen('images/deadSmiley.png')
	if smiley is None:
		smiley = pui.locateCenterOnScreen('images/winSmiley.png')
	if smiley is None:
		print('Can not start game!')
		exit()
	smiley = (smiley[0]//2, smiley[1]//2)
	pui.click(smiley)
	pui.click(smiley)
	left, right, top, bot = locate_playing_field()

	squareDelta = (right-left)//(width-1)
	#These are the coordinates of the squares in the game
	xLocs = [x*squareDelta+left for x in range(width)]
	yLocs = [y*squareDelta+top for y in range(height)]

	screenRegion['width'] = right+6
	screenRegion['height'] = bot+6

	return (xLocs, yLocs)

def is_closed(x, y, screen):
	return screen.getpixel((x*2, y*2-18))[0:3] == (255,255,255)

def find_square_value(x, y, screen):
	if is_closed(x, y, screen): return 9 #9 represents a closed square
	if screen.getpixel((x*2, y*2))[0:3] == (0  ,39 ,244): return 1
	if screen.getpixel((x*2, y*2+3))[0:3] == (56 ,120,33 ): return 2
	if screen.getpixel((x*2+6, y*2))[0:3] == (233,50 ,35 ): return 3
	if screen.getpixel((x*2, y*2-4))[0:3] == (0  ,13 ,117): return 4
	if screen.getpixel((x*2, y*2-4))[0:3] == (112,19 ,11 ): return 5
	if screen.getpixel((x*2-4, y*2))[0:3] == (54 ,121,122): return 6
	if screen.getpixel((x*2+6, y*2))[0:3] == (4  ,4  ,4  ): return 7
	if screen.getpixel((x*2, y*2))[0:3] == (123,123,123): return 8
	if screen.getpixel((x*2, y*2))[0:3] == (189,189,189): return 0
	if screen.getpixel((x*2, y*2))[0:3] == (0  ,0  ,0): 
		print(board.T)
		print('LOST!')
		exit() #bomb
	print('ERROR NO VALUE FOUND FOR SQUARE {} {}!!!'.format(x, y))
	print('color is {}'.format(screen.getpixel((x*2, y*2))[0:3]))
	print(board.T)
	exit()

def update_board(xLocs, yLocs):
	screenshot = mss.mss().grab(screenRegion)
	screen = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

	for i, x in enumerate(xLocs):
		for j, y in enumerate(yLocs):
			if board[i][j] != -1:
				board[i][j] = find_square_value(x, y, screen) 


def get_surrounding(xi, yi):
	bombs = []
	hidden = []
	for i in range(-1, 2):
		x = xi+i
		for j in range(-1, 2):
			y = yi+j
			if y >= 0 and x >= 0 and y < height and x < width:
				if i != 0 or j != 0:
					if board[x][y] == -1: bombs.append((x,y))
					if board[x][y] == 9: hidden.append((x,y))
	return bombs, hidden

def open_squares(xLocs, yLocs):
	activity = False
	for i, x in enumerate(xLocs):
		for j, y in enumerate(yLocs):
			if board[i][j] > 0 and board[i][j] < 9:
				bombs, hidden = get_surrounding(i, j)
				if len(bombs) == board[i][j] and len(hidden) > 0:
					activity = True
					for x,y in hidden:
						board[x][y] = 8 #tries to prevent clicking the same square again later
						pui.click(xLocs[x], yLocs[y], button='left')
	if activity == False:
		make_guess(xLocs, yLocs)

# def click_surrounding(xLocs, yLocs):

def make_guess(xLocs, yLocs):
	print('Guessing')
	for i, x in enumerate(xLocs):
		for j, y in enumerate(yLocs):
			if board[i][j] == 9:
				pui.click(xLocs[i], yLocs[j])
				return

def find_bombs(xLocs, yLocs):
	for i, x in enumerate(xLocs):
		for j, y in enumerate(yLocs):
			if board[i][j] > 0 and board[i][j] < 9:
				bombs, hidden = get_surrounding(i, j)
				if len(bombs) + len(hidden) == board[i][j]:
					for x,y in hidden:
						board[x][y] = -1
						#include the line below to mark the bombs on screen
						#pui.click(xLocs[x], yLocs[y], button='right')

def play_game():
	xLocs, yLocs = start_game()
	pui.click(xLocs[width//2], yLocs[height//2])

	count = 0
	while count < 50:
		# start = time.time()
		# print('starting ')
		update_board(xLocs, yLocs)
		# print('finished updating board ' + str(time.time()-start))
		# start = time.time()
		find_bombs(xLocs, yLocs)
		# print('finished finding bombs ' + str(time.time()-start))
		# start = time.time()
		open_squares(xLocs, yLocs)
		# print('finished double clicking ' + str(time.time()-start))
		count += 1

# import time
play_game()
print(board.T)


