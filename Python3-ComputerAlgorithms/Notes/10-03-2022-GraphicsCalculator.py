# Gather the user's input and graph it

import math
from graphics import *

def infixToPostfix():
    pass

def evaluatePostfix():
    pass

def printDirections():
    pass

def main():
    printDirections()
    infixFunction = input("Enter your function here: ")
    # Convert from infix to postfix; easier to parse and work with
    postfixFunction = infixToPostfix(infixFunction)
    
    win = GraphWin("My Parabola", 900, 900)

    xLow = -10
    xHigh = 10
    yLow = -10
    yHigh = 10
    xInc = .1

    win.setCoords(xLow, yLow, xHigh, yHigh)
    x = xLow
    while x < xHigh:
        y = evaluatePostfix(postfixFunction, x)
        x2 = x+xInc
        y2 = evaluatePostfix(postfixFunction, x2)
        line = Line(Point(x,y), Point(x2,y2))
        line.setWidth(3)
        line.setOutline("red")
        line.draw(win)
        x += xInc
    
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()

# Example of RPN
# 2 6 + 5 1 + 4 * /
# 8     24
# 1/3