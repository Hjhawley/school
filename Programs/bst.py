# Binary search tree

from node import Node

class BST:

    def __init__(self):
        self.mRoot = None

    def insert(self, item):
        if self.exists(item):
            return False
        n = Node(item)
        self.mRoot = self.insertR(n, self.mRoot)
        return True

    def insertR(self, n, current):
        if current is None:
            current = n
        elif n.mItem < current.mItem: # Walk down the tree
            current.mL = self.insertR(n, current.mL)
        else:
            current.mR = self.insertR(n, current.mR)
    
    def retrieve(self, item):
        return retrieveR(item, self.mRoot)
    
    def retrieveR(self, item, current):
        if current is None:
            return None
        elif item == current.mItem:
            return current.mItem
        elif item < current.mItem:
            return self.retrieveR(item, current.mL)
        else:
            return self.retrieveR(item, current.mR)
    
    def size(self):
        return self.sizeR(self.mRoot)
    
    def sizeR(self, current):
        if current is None:
            return 0
        count = 1
        count += sizeR(current.mL)
        count += sizeR(current.mR)
        return count
    
    def traverse(self, callback, data):
        current = self.mRoot
        self.traverseR(callback, data, current)
    
    def traverseR(self, callback, data, current):
        if current is None: # == ?
            return
        callback(current.mItem.data)
        self.traverseR(callback, data, current.mL)
        self.traverseR(callback, data, current.mR)
    
    def exists(self, item):
        exist = self.existsR(item, self.mRoot)
        return exist
    
    def existsR(self, n, current):
        if current is None:
            return False
        elif current.mItem == nItem:
            return True
        elif n.mItem < current.mItem:
            return self.existsR(n, current.mL)
        else:
            return self.existsR(n, current.mR)