"""
You have a 5-gallon jug and a 3-gallon jug, both initially empty. Your goal is to have exactly
4 gallons of water in the 5-gallon jug, and 0 gallons in the 3-gallon jug.

You are allowed the following operations:
1. Fill any of the jugs completely.
2. Pour water from one jug into the other until the first jug is empty or the second jug
is full.
3. Empty the contents of a jug.

Objectives:

1. Describe a method to reach the goal state (4 gallons in the 5-gallon jug and 0
gallons in the 3-gallon jug). You can solve this puzzle step by step in any way that
works, without needing to apply a general algorithm. Assume (m, n) denote m gallons
in the 5-gallon jug and n gallons in the 3-gallon jug.

Example
(a) Start with empty jugs: (0, 0)
(b) Fill jug 3: (0, 3)
(c) Pour from jug 3 to jug 5: (3, 0)
(d) Fill jug 3: (3, 3)
(e) ...
(f) Pour from jug 3 to jug 5: (4, 0) (Goal reached)

2. Now we generalize the problem to two jugs of any size, and we hope to find
steps to reach a target volume in one jug, e.g. two jugs of 7 and 5 gallons for a target
of 6 gallons. Write a program to automate the solution to this problem. The program
should find the minimum number of steps and print each step taken to reach the goal
state.

Function definition:
reach_target_volume(size_A, size_B, target_vol)

Output:
Steps for size_A=7, size_B=5, target_vol=6:
(0, 0)
(7, 0)
(2, 5)
...
(6, 5)

If there is no solution, return: "unreachable"

Hint: Treat each state of the jugs as a vertex (m, n), where m and n are the amounts of
water in the jugs. Operations (filling, pouring, emptying) are edges between states. Use
Breadth-First Search (BFS) to find the shortest path from the initial state (0, 0) to the
target state (x, y) or return "unreachable".
"""

from collections import deque

def reach_target_volume(size_A, size_B, target_vol):
    # greatest common divisor
    # target volume is achievable only if it is a multiple of the GCD of the two jug sizes
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    if target_vol > max(size_A, size_B) or target_vol % gcd(size_A, size_B) != 0:
        return "unreachable"
    
    visited = set()
    parent = {}   # To reconstruct the path
    q = deque()
    start = (0, 0)
    q.append(start)
    visited.add(start)
    parent[start] = None

    while q:
        current = q.popleft()
        a, b = current
        if a == target_vol or b == target_vol:
            # Reconstruct the path
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # reverse the path
        
        next_states = []
        # Fill jug A
        next_states.append((size_A, b))
        # Fill jug B
        next_states.append((a, size_B))
        # Empty jug A
        next_states.append((0, b))
        # Empty jug B
        next_states.append((a, 0))
        # Pour A -> B
        pour = min(a, size_B - b)
        next_states.append((a - pour, b + pour))
        # Pour B -> A
        pour = min(b, size_A - a)
        next_states.append((a + pour, b - pour))
        
        for state in next_states:
            if state not in visited:
                visited.add(state)
                parent[state] = (a, b)
                q.append(state)
    
    return "unreachable"

def main():
    # Example 1: 5-gallon and 3-gallon jugs with target 4 gallons.
    print("Example 1: size_A=6, size_B=4, target_vol=1")
    result = reach_target_volume(6, 4, 1)
    if result == "unreachable":
        print("unreachable")
    else:
        for step in result:
            print(step)
    print()

    # Example 2: 7-gallon and 5-gallon jugs with target 6 gallons.
    print("Example 2: size_A=11, size_B=5, target_vol=8")
    result = reach_target_volume(11, 5, 8)
    if result == "unreachable":
        print("unreachable")
    else:
        for step in result:
            print(step)

if __name__ == "__main__":
    main()
