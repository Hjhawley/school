"""
You have a collection of books and need to arrange them on shelves by color. Each shelf
can hold only books of the same color, but you don't know the colors directly. Instead, you
are given pairs of books known to be the same color. This relation follows an equivalent
relation (reflexive, symmetric, and transitive). Your task is to write a code to determine the
minimum number of shelves needed, ensuring that no two books of different colors share a shelf.
"""

def dfs(book, visited, graph):
    stack = [book]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

def min_shelves(books, pairs):
    # Build an undirected graph
    # Any group of books connected by pairs will all be the same color (connected components)
    graph = {book: [] for book in books}
    for a, b in pairs:
        graph[a].append(b)
        graph[b].append(a)
    
    visited = set() # keep tracks of books we've seen
    shelves = 0
    
    for book in books:
        if book not in visited:
            dfs(book, visited, graph)
            shelves += 1
    return shelves
