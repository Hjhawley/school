# Binary search tree

from node import Node

class BST:
    
    def __init__(self):
        pass

    def insert(self, item):
        if self.exists(item):
            return False
        n = Node(item)
        self.mRoot = self.insertR(n, self.mRoot)
        return True

    def insertR(self, n, current):
        if current is None:
            current = n
        elif n.mItem < current.mItem:
            current.mR = self.insertR(n, current.mR)