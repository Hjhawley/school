# Directed, unweighted graph

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
        pass