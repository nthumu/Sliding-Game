import copy
import random

import pygame
import sys

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
#  window dimensions
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BGCOLOR = BLACK
LIGHTBGCOLOR = GRAY
#  Board dimensions
BOARDWIDTH = 4
BOARDHEIGHT = 4

#  Box details
BOXSIZE = 80
GAPSIZE = 6
BOXCOLOR = GREEN
HIGHLIGHTCOLOR = RED

BOARDDIMNS = 350
BOARDCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)



def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return left, top


def generateSolvedBoard():

    solvedBoard = {}
    counter = 1
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if boxx == BOARDWIDTH-1 & boxy == BOARDHEIGHT-1:
                solvedBoard[(boxx, boxy)] = None
            else:
                solvedBoard[(boxx, boxy)] = counter
                counter += BOARDWIDTH
        counter -= (BOARDWIDTH * BOARDHEIGHT) - 1
    return solvedBoard


def drawBoard(board):
    for key, value in board.items():
        left, top = leftTopCoordsOfBox(key[0], key[1])
        if value is not None:
            boxRect = pygame.Rect((left, top, BOXSIZE, BOXSIZE))
            fontObj = pygame.font.Font('freesansbold.ttf', 32)
            textSurfObj = fontObj.render(str(value), True, WHITE, GREEN)
            textRectObj = textSurfObj.get_rect()
            textRectObj.center = boxRect.center
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE,
                                                     BOXSIZE))
            DISPLAYSURF.blit(textSurfObj, textRectObj)
        else:
            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, BOXSIZE,
                                                  BOXSIZE))
    pygame.display.update()


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != BOARDHEIGHT - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != BOARDWIDTH - 1) or \
           (move == RIGHT and blankx != 0)

def generateRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    # return a random move from the list of remaining moves
    return random.choice(validMoves)

def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDWIDTH):
            if board[(x, y)] == None:
                return x, y


def updateBoard(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[(blankx, blanky)] = board[(blankx, blanky + 1)]
        board[(blankx, blanky + 1)] = None
    elif move == DOWN:
        board[(blankx, blanky)] = board[(blankx, blanky - 1)]
        board[(blankx, blanky - 1)] = None
    elif move == LEFT:
        board[(blankx, blanky)] = board[(blankx + 1, blanky)]
        board[(blankx + 1, blanky)] = None
    elif move == RIGHT:
        board[(blankx, blanky)] = board[(blankx - 1, blanky)]
        board[(blankx - 1, blanky)] = None


def generateShuffledBoard():

    # Select the valid number of moves from the list.
    numOfMoves = [80]
    lastMove = None
    board = generateSolvedBoard()
    for move in range(random.choice(numOfMoves)):
        slideTo = generateRandomMove(board, move)
        updateBoard(board, slideTo)
        drawBoard(board)
        pygame.display.update()


    return board
    # 1. generate a valid move by using random module
    # 2. draw the board
    # 3. return the randomly generated board.





def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                     (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def checkForEmptyBox(boxx, boxy, board):
    #  check for empty boxes in the row.

    for row in range(boxy-1, boxy+2):
        if row >= 0 and row < 4:
            if board[(boxx, row)] is None:
                return (boxx, row)
    for column in range(boxx-1, boxx+2):
        if column >= 0 and column < 4:
            if board[(column, boxy)] is None:
                return (column, boxy)
    return None

def slideBox(boxx, boxy, emptyBox):
    CRNTSTATOFBOXES[emptyBox] = CRNTSTATOFBOXES[(boxx, boxy)]
    CRNTSTATOFBOXES[(boxx, boxy)] = None
    drawBoard(CRNTSTATOFBOXES)

def hasWon(CRNTSTATOFBOXES):
    winBoxes = {(0, 0): 1, (0, 1): 5, (0, 2): 9, (0, 3): 13,
                (1, 0): 2, (1, 1): 6, (1, 2): 10, (1, 3): 14,
                (2, 0): 3, (2, 1): 7, (2, 2): 11, (2, 3): 15,
                (3, 0): 4, (3, 1): 8, (3, 2): 12, (3, 3): None}

    for key, value in CRNTSTATOFBOXES.items():
        if CRNTSTATOFBOXES[key] != winBoxes[key]:
            return False
    return True

def gameWonAnimation(CRNTSTATOFBOXES):
    # flash the background color when the player has won
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(CRNTSTATOFBOXES)
        pygame.display.update()
        pygame.time.wait(300)

def main():
    global DISPLAYSURF, ALLMOVES, CRNTSTATOFBOXES
    #  Draw a Board with shuffled boxes
    pygame.init()
    ALLMOVES = []
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    #  Creating an object of a window.
    windowRect = DISPLAYSURF.get_rect()
    #  below line - Creating an Object of a rectange
    boardRect = pygame.Rect(windowRect.centerx, windowRect.centery, BOARDDIMNS,
                            BOARDDIMNS)
    #  below line - assigning the center of the window to the rectangle's
    #  center.
    boardRect.center = windowRect.center

    pygame.draw.rect(DISPLAYSURF, BOARDCOLOR, boardRect)
    SOLVEDBOARD = generateSolvedBoard()
    drawBoard(SOLVEDBOARD)
    pygame.time.wait(250)
    pygame.display.update()
    CRNTSTATOFBOXES = generateShuffledBoard()

    mousex = 0
    mousey = 0
    while True:
        mouseClicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            emptyBox = checkForEmptyBox(boxx, boxy, CRNTSTATOFBOXES)
            if emptyBox is not None and mouseClicked:
                # if not hasWon(CRNTSTATOFBOXES):
                if SOLVEDBOARD != CRNTSTATOFBOXES:
                    slideBox(boxx, boxy, emptyBox)
                else:
                    gameWonAnimation(CRNTSTATOFBOXES)

        pygame.display.update()

if __name__ == '__main__':
    main()
