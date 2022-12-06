# Directed, unweighted graph

from queue import Queue

class Graph:
    
    def __init__(self, numVertices):
        self.mVertices = numVertices
        self.mNeighbors = [numVertices*[]] # A list of lists
    
    def addEdge(self, v0, v1):
        self.mNeighbors[v0] = v1
        return True

    def isEdge(self, v0, v1):
        isEdge = v1 in self.mNeighbors[v0]
        return isEdge

    def getNeighbors(self, v0):
        return self.mNeighbors[v0]

    def findPath(v0, v1):
        # Shortest path or return None
        q = Queue()
        cameFrom = [-1] * len(self.mNeighbors) # -1 means "not visited yet"
        q.enqueue(v0)
        cameFrom[v0] = v0
        # While the queue is not empty:
            c = q.dequeue() # Make c the current vertex
            if c == v1:
                # Build a path and return it
            for all neighbors "n" of c
                # If not visited yet (-1)
                    # enqueue n
                    # mark that n came from c
        return None