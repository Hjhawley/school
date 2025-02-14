"""
You have a collection of books and need to arrange them on shelves by color. Each shelf
can hold only books of the same color, but you don't know the colors directly. Instead, you
are given pairs of books known to be the same color. This relation follows an equivalent
relation (reflexive, symmetric, and transitive). Your task is to write a code to determine the
minimum number of shelves needed, ensuring that no two books of different colors share a shelf.
"""

def min_shelves(books, pairs):
    # Build the graph (adjacency list)
    graph = {book: [] for book in books}
    for u, v in pairs:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    shelves = 0
    
    def dfs(book):
        stack = [book]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
    
    for book in books:
        if book not in visited:
            dfs(book)
            shelves += 1
    return shelves
