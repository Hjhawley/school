# Directed, unweighted graph

from myqueue import Queue

class Graph:
    
    def __init__(self, numVertices):
        self.mVertices = numVertices
        self.mNeighbors = [[] for i in range(numVertices)] # A list of lists
    
    def addEdge(self, v0, v1):
        self.mNeighbors[v0].append(v1)
        return True

    def isEdge(self, v0, v1):
        isEdge = v1 in self.mNeighbors[v0]
        return isEdge

    def getNeighbors(self, v0):
        return self.mNeighbors[v0]

    def findPath(self, v0, v1):
        # Shortest path or return None
        q = Queue()
        cameFrom = [-1] * len(self.mNeighbors) # -1 means "not visited yet"
        q.enqueue(v0)
        cameFrom[v0] = v0
        while not q.isEmpty():  # While the queue is not empty:
            c = q.dequeue()     # Make c the current vertex
            if c == v1:
                # Build a path and return it
                path = [c]
                while c != v0:
                    c = cameFrom[c]
                    path.append(c)
                path.reverse()
                return path
            for n in self.mNeighbors[c]:
                if cameFrom[n] == -1:   # If not visited yet
                    q.enqueue(n)
                    cameFrom[n] = c     # Mark that n came from c
        return None # If no valid path