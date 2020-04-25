import pprint as pp
import random
import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib.animation as animation
from copy import deepcopy

# Setting: set to true if you want to save the animation locally
saveFile = True
# Setting: file name of the saved animation if saveFile is True
fileName = 'gof.gif'
# Setting: speed of animation in ms
animationSpeed = 10
# Setting: number of frames (how long) for animation
animationFrames = 80
# Setting: random generated size of board (lenght and height) with specified min max range
boardSize = random.randint(50, 300)
# Setting: ratio of dead vs. alive respectively in percentage
deadAliveChances = [95, 5]


def main():
    """Entry point of script"""

    showAnimation(generateBoard())
    #showAnimation(generateBoardTest(100, 'acorn'))


def generateBoard():
    """Returns a random genereated board to represent the starting state"""

    return [random.choices([0,1], deadAliveChances, k=boardSize) for _ in range(boardSize)]


def generateBoardTest(size, pattern):
    """Returns an initialized board for testing purposes. Size of board and pattern can be specified.
    
    Patterns supported: glider, acorn, blinker, and beacon
    """

    size = 20 if size < 10 else size
    board = [[0 for col in range(size)] for row in range(size)]

    if pattern == 'glider':
        board[0][1] = 1
        board[1][2] = 1
        board[2][0] = 1
        board[2][1] = 1
        board[2][2] = 1
    elif pattern == 'acorn':
        middleIndex = round(size / 2)
        board[middleIndex][middleIndex + 1] = 1
        board[middleIndex + 1][middleIndex + 3] = 1
        board[middleIndex + 2][middleIndex] = 1
        board[middleIndex + 2][middleIndex + 1] = 1
        board[middleIndex + 2][middleIndex + 4] = 1
        board[middleIndex + 2][middleIndex + 5] = 1
        board[middleIndex + 2][middleIndex + 6] = 1
    elif pattern == 'blinker':
        middleIndex = round(size / 2)
        board[middleIndex - 1][middleIndex] = 1
        board[middleIndex][middleIndex] = 1
        board[middleIndex + 1][middleIndex] = 1
    elif pattern == 'beacon':
        middleIndex = round(size / 2)
        board[middleIndex - 1][middleIndex - 2] = 1
        board[middleIndex - 1][middleIndex - 1] = 1
        board[middleIndex][middleIndex - 2] = 1
        board[middleIndex][middleIndex - 1] = 1
        board[middleIndex + 2][middleIndex + 1] = 1
        board[middleIndex + 2][middleIndex] = 1
        board[middleIndex + 1][middleIndex] = 1
        board[middleIndex + 1][middleIndex + 1] = 1
    
    return board


def getNextGeneration(board):
    """Returns the next state of the board by applying the rules"""

    newBoard = deepcopy(board)

    for indexRow in range(len(board)):
        for indexCol in range(len(board[0])):
            newBoard[indexRow][indexCol] = getNewState(indexRow, indexCol, board)
    
    return newBoard


def printGenerationsToConsole(board):
    """Prints the board in console for debugging/testing purposes"""

    print('== PRINTING GENERATIONS: ')
    numOfGenerations = 2
    generations = []
    generations.append(board)

    previousBoard = board

    for _ in range(numOfGenerations - 1):
        newBoard = getNextGeneration(previousBoard)
        generations.append(newBoard.copy())
        previousBoard = newBoard

    for board in generations:
        for b in board:
            pp.pprint(b)
        print()


def update(frameNum, img, board, N):
    """Function to be called by matplotlib.animation to create the succeeding frames"""

    newBoard = getNextGeneration(board)
    img.set_data(newBoard)
    board[:] = newBoard[:]
    return img, 


def showAnimation(startingBoard):
    """Shows the animation using matplotlib by using startingBoard as the first frame and calls update for succeeding frames"""

    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(
                        fig,
                        update, 
                        fargs = (ax.imshow(startingBoard, interpolation='nearest'), startingBoard, len(startingBoard), ), 
                        frames = animationFrames, 
                        interval = animationSpeed, 
                        save_count = 10) 

    if saveFile:
        ani.save(fileName, writer='imagemagick', fps=20)

    plt.show()


def getNewState(indexRow, indexCol, board):
    """Returns the new state (dead or alive) of a cell in the board"""

    aliveNeighbors = 0
    boardSize = len(board) - 1

    #Loops through each neighboring cell and counts all alive cells
    for row in [r for r in range(-1, 2) if (indexRow + r >= 0) and (indexRow + r <= boardSize)]:
        for col in [c for c in range(-1, 2) if (indexCol + c >= 0) and (indexCol + c <= boardSize)]:
            if (indexRow + row == indexRow and indexCol + col == indexCol):
                continue
            if board[indexRow + row][indexCol + col] == 1:
                aliveNeighbors += 1

    if board[indexRow][indexCol] == 1:
        if aliveNeighbors == 2 or aliveNeighbors == 3:
            return 1
    elif aliveNeighbors == 3:
            return 1
    return 0


main()