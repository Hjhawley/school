from collections import deque

def reach_target_volumn(size_A, size_B, target_vol):
    # Check if the target is reachable.
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
