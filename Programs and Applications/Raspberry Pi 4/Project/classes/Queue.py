class Queue(object):
    """FIFO Logic"""
    def __init__(self):
        self.__item = []

    def enqueue(self, add):
        self.__item.insert(0, add)
        return True

    def dequeue(self):
        if not self.is_empty():
            return self.__item.pop()

    def is_empty(self):
        if self.__item:
            return True
        return False
