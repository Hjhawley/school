from lib2to3.pytree import Node

class UUC:
    def __init__(self):
        self.mFirst = None
        
    def delete(self, item):
        if not self.exists(item):
            return False
        if self.mFirst.mItem == item:
            self.mFirst = self.mFirst.mNext
        current = self.mFirst
        while not(current.mNext.mItem == item):
            current = current.mNext
        current.mNext = current.mNext.mNext
        return True

    def size(self):
        count = 0
        current = self.mFirst
        while not (current == None):
            count += 1
            current = current.mNext
        return count

    def traverse(self, callback):
        current = self.mFirst
        while not (current == None):
            callback(current.mItem)
            current = current.mNext

    def exists(self, item):
        current = self.mFirst
        while current:
            if current.mItem == item:
                return True
            current = current.mNext
        return False

    def retrieve(self, item):
        if not self.exists(item):
            return None
        current = self.mFirst
        while not (current.mItem == item):
            current = current.mNext
        return current

    def insert(self, item):
        if self.exists(item):
            return False
        else:
            self.mFirst = Node(item, self.mFirst)
            return True