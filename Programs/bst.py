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
        return current
    
    def retrieve(self, item):
        return self.retrieveR(item, self.mRoot)
    
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
        count += self.sizeR(current.mL)
        count += self.sizeR(current.mR)
        return count
    
    def traverse(self, callback, data):
        current = self.mRoot
        self.traverseR(callback, data, current)
    
    def traverseR(self, callback, data, current):
        if current is None:
            return
        callback(current.mItem.data)
        self.traverseR(callback, data, current.mL)
        self.traverseR(callback, data, current.mR)
    
    def exists(self, item):
        exist = self.existsR(item, self.mRoot)
        return exist
    
    def existsR(self, i, current):
        if current is None:
            return False
        elif current.mItem == i:
            return True
        elif i < current.mItem:
            return self.existsR(i, current.mL)
        else:
            return self.existsR(i, current.mR)

    def delete(self, item):
        if not self.exists(item):
            return False
        else:
            self.mRoot = self.deleteR(item, self.mRoot)
            return True
    
    def deleteR(self, item, current):
        if current.mItem == item:
            if current.mL is None and current.mR is None:       # Leaf node
                current = None
            elif current.mL is None and current.mR is not None: # One child on the right
                current = current.mR
            elif current.mL is not None and current.mR is None: # One child on the left
                current = current.mL
            else:                                               # Two children
                walkdown = current.mR                           # Walk down to find the in-order successor
                while walkdown.mL:
                    walkdown = walkdown.mL
                current.mItem = walkdown.mItem
                current.mR = self.deleteR(current.mItem, current.mR)
        elif item < current.mItem:
            current.mL = self.deleteR(item, current.mL)
        elif item > current.mItem:
            current.mR = self.deleteR(item, current.mR)
        return current