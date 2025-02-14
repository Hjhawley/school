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
