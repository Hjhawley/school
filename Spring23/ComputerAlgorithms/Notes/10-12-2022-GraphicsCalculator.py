# Gather the user's input and graph it

import math
from stack import Stack
from graphics import *

def infixToPostfix(infix):
    postfix = ""
    s = Stack()
    for c in infix:
        if (c >= '0' and c <= '9') or c == 'x':
            postfix += c
        elif c == '(':
            s.push(c)
        elif c == ')':
            parenthetical = s.pop()
            while parenthetical != '(':
                postfix += parenthetical
                parenthetical = s.pop()
            s.pop() # Discard '('
        elif c in "*/":
            if s.isEmpty() or s.top() in '+-(':
                s.push(c)
            else:
                while s.top() in "*/":
                    postfix += s.pop()
                s.push(c)
        elif c in '+-':
            if s.isEmpty() or s.top() == '(':
                s.push(c)
            else:
                while s.isEmpty() == False and s.top() in '+-*/':
                    postfix += s.pop()
                s.push(c)
    while not s.isEmpty():
        postfix += s.pop() # Pop the rest of the stack to postfix
    return postfix

# Test

infix = '3 * (4 + 5 - 1) / 6 + x'
postfix = infixToPostfix(infix)
print(postfix)

#postfix: "3 4 5 + 1 - * 6 / x +"

def printDirections():
    print("This program allows the user to enter a math equation, then draws it.") # Add more info

'''

def evaluatePostfix():
    pass



def main():
    printDirections()
    infixFunction = input("Enter your function here: ")
    # Convert from infix to postfix; easier to parse and work with
    postfixFunction = infixToPostfix(infixFunction)
    
    win = GraphWin("Graphing Calculator", 900, 900)

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

'''