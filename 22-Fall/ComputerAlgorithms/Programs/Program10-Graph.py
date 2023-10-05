'''
Graph: Breadth-First Search
Implement a non-weighted, directed Graph data structure.
Store the data using a list of neighbors for each vertex.
Implement all the required methods as discussed in class.

Write a main function that loads a graph from an input file.
Note that YOU need to make the input file using a text editor, with the following specification:
The first line of the input file contains the number of vertices.
The second line contains the number of edges.
The next several lines contain pairs of vertex indices, one for each edge, indicated there is a directed edge from the first vertex to the second.
The next line contains the number of test cases.
The next several lines contains pairs of vertex indices, one for each test, asking for a path from the first to the second, or 'None.'

After loading the graph information, call the graph's BreadthFirstSearch method to find a path (or 'None') for all of the test cases.
Be sure to include at least one test case that has a path, and one that does not have a solution.
'''

from graph import Graph

def main():
    f = open("data.txt")
    numV = int(f.readline())    # This should be '9'
    g = Graph(numV)             # Create a graph with 9 vertices
    numE = int(f.readline())    # This should be '13'
    for i in range(numE):
        words = f.readline().split() # This line becomes a list of two strings
        g.addEdge(int(words[0]), int(words[1]))
    numT = int(f.readline())
    for i in range(numT):
        words = f.readline().split()
        print(g.findPath(int(words[0]), int(words[1])))
    f.close()

main()