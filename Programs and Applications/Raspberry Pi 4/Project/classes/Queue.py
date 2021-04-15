class Queue(object):
    def __init__(self):
        self.item = []

    def enqueue(self, add):
        self.item.insert(0, add)
        return True

    def size(self):
        return len(self.item)

    def isEmpty(self):
        if self.size() == 0:
            return True
        else:
            return False

    def dequeue(self):
        if self.isEmpty():
            return None
        else:
            return self.item.pop(0)

    def clear(self):
        self.item = []

    def getData(self):
        return self.item
