# Hash Table

from math import sqrt

def isPrime(x):
    s = int(sqrt(x))
    for i in range (2, s+1):
        if x % i == 0:
            return False
    return True

class Hash:

    def __init__(self, desiredCount):
        actualCount = 2 * desiredCount + 1
        while not isPrime(actualCount):
            actualCount += 2 # Skip the evens to save time
        self.mTable = [None] * actualCount

    def insert(self, item):
        if self.exists(item):
            return False
        key = int(item)
        index = key % len(self.mTable)
        while self.mTable[index]:
            index += 1
        self.mTable[index] = item
        return True

    def retrieve(self, item):
        if not self.exists(item):
            return False
        else:
            key = int(item)
            index = key % len(self.mTable)
            while not self.mTable[index] == item:
                index += 1
                if index == len(self.mTable):
                    index = 0
            return self.mTable[index]
    
    def exists(self, item):
        key = int(item)
        index = key % len(self.mTable)
        while True:
            if self.mTable[index] is None:
                return False
            elif self.mTable[index] and self.mTable[index] == item:
                return True
            index += 1
            if index == len(self.mTable):
                index = 0
    
    def size(self):
        count = 0
        for i in self.mTable:
            if i: # If not None or False
                count += 1
        return count
    
    def traverse(self, callback):
        for i in self.mTable:
            if i:
                callback(i)
    
    def delete(self, item):
        if not self.exists(item):
            return False
        else:
            key = int(item)
            index = key % len(self.mTable)
            while not self.mTable[index] == item:
                index += 1
                if index == len(self.mTable):
                    index = 0
            self.mTable[index] = False
            return True