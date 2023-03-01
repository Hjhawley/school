class Queue:

    def __init__(self):
        self.mData = []

    def __len__(self):
        return len(self.mData)

    def enqueue(self, item):
        self.mData.append(item)

    def dequeue(self):
        return self.mData.pop(0)

    def isEmpty(self):
        return (self.mData == [])

    def front(self):
        return self.data(0)