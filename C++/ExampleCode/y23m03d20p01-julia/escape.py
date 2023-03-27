#!/usr/bin/env python3

import math

def f(x, y):
    a = 0.1
    b = 0.22
    x1 = x*x - y*y + a
    y1 = 2*x*y + b
    return x1, y1

def did_not_escape(x, y):
    if math.sqrt(x*x + y*y) <= 2:
        r = True
    else:
        r = False
    return r

def calculatePlaneEscapeCount(x0, y0):
    max_escape_count = 100
    x_in, y_in = x0, y0
    escape_count = 0
    while did_not_escape(x_in, y_in) and (escape_count < max_escape_count):
        escape_count += 1
        x_out, y_out = f(x_in, y_in)
        x_in, y_in = x_out, y_out
        
    return escape_count


escape_count = calculatePlaneEscapeCount(0.5, 0.6)

