# Draw a parabola

from graphics import *

def main():
    win = GraphWin("My Parabola", 900, 900)

    xLow = -10
    xHigh = 10
    yLow = -10
    yHigh = 10
    xInc = .1

    win.setCoords(xLow, yLow, xHigh, yHigh)
    x = xLow
    while x < xHigh:
        y = x*x
        x2 = x+xInc
        y2 = x2*x2
        line = Line(Point(x,y), Point(x2,y2))
        line.setWidth(3)
        line.setOutline("red")
        line.draw(win)
        x += xInc

    ''' For loops don't work with Floats
    for x in range(xLow, xHigh+1, xInc):
        y = x*x
        x2 = x+1
        y2 = x2*x2
        line = Line(Point(x,y), Point(x2,y2))
        line.draw(win)
        '''
    
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()