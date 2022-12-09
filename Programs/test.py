LofL = [[], [1], [1, 2]]
cameFrom = [-1, 2, 3]

for n in range(len(LofL)):
    if cameFrom[n] == -1:
        print("NVY")
    else:
        print(n)