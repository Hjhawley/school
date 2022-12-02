# Binary search tree

from node import BSTNode

class BST:

    def __init__(self):
        self.mRoot = None

    def insert(self, item):
        if self.exists(item):
            return False
        n = BSTNode(item)
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
    
    def delete(self, item):
        parent = None
        return self.deleteR(item, self.mRoot, parent)
    
    def deleteR(self, item, current, parent):
        if current is None:
            return False
        elif item < current.mItem:
            parent = current
            self.deleteR(item, current.mL)
        elif item > current.mItem:
            parent = current
            self.deleteR(item, current.mR)
        else: # We've found the node to delete
            if current.mL is None and current.mR is None:   # Leaf node
                if parent.mL.mItem == current.mItem:
                    parent.mL = None
                else:
                    parent.mR = None
            if current.mL is None ^ current.mR is None:     # Branch with one child
                if parent.mL.mItem == current.mItem:
                    parent.mL = current.mL
                else:
                    parent.mR = current.mR
            else:                                           # Branch with two children
                pass # LEAST IN ORDER SUCCESSOR