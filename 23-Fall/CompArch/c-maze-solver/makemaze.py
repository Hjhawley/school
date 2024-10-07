#!/usr/bin/env python3

# generate a maze using a simple but not very good approach

import random

wall = '@'
path = '.'

# get a random size and make sure both dimensions are odd
(sizex, sizey) = (99, 49)

# start with a field of all walls
field = [[wall] * sizex for i in range(sizey)]

# seed it with a path in one spot
field[random.randrange(sizey-1)|1][random.randrange(sizex-1)|1] = path

# now randomly extend paths outward from existing paths
# until the maze is fully formed
extensions_needed = (sizex // 2) * (sizey // 2) - 1;
extensions_added = 0
while extensions_added < extensions_needed:
    # pick a spot where a path could go
    (x, y) = (random.randrange(sizex-1)|1, random.randrange(sizey-1)|1)
    if field[y][x] == path:
        continue

    # pick a direction
    (dx, dy) = random.choice( ((-1,0), (1,0), (0,-1), (0,1)) )

    # make sure it does not lead us off the field
    if x+dx+dx < 1 or x+dx+dx > sizex-1 or y+dy+dy < 1 or y+dy+dy > sizey-1:
        continue

    # must be a path in that direction
    if field[y+dy+dy][x+dx+dx] != path:
        continue

    # success! add an extension
    field[y][x] = path
    field[y+dy][x+dx] = path
    extensions_added += 1

# create start and end points
field[1][0] = path
field[sizey-2][sizex-1] = path

# print the result
for row in field:
    print(''.join(row))
