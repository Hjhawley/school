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
    # Each book maps to its list of connected books
    graph = {book: [] for book in books}
    for a, b in pairs:
        graph[a].append(b)
        graph[b].append(a)
    
    visited = set()
    shelves = 0
    
    # For each book, if it hasn't been visited, explore its connected component
    for book in books:
        if book not in visited:
            dfs(book, visited, graph)
            shelves += 1
    return shelves

def main():
    # Get input for books as a comma-separated list
    books_input = input("Enter the books (comma-separated, e.g. a, b, c): ")
    # Split on commas and strip whitespace from each book name
    books = [book.strip() for book in books_input.split(",") if book.strip()]
    
    # Get input for pairs.
    # Each pair should be two books separated by whitespace,
    # and pairs separated by commas. E.g., "a b, c d, e f"
    pairs_input = input("Enter the pairs (each pair as two books separated by space, pairs separated by commas, e.g. a b, c d): ")
    pairs = []
    # Split the input by commas to get each pair
    for pair_str in pairs_input.split(","):
        pair_str = pair_str.strip()
        if pair_str:
            # Split the pair by whitespace to get the two books
            parts = pair_str.split()
            if len(parts) == 2:
                pairs.append((parts[0], parts[1]))
            else:
                print(f"Skipping invalid pair: {pair_str}")
    
    result = min_shelves(books, pairs)
    print("Minimum number of shelves needed:", result)

if __name__ == "__main__":
    main()
