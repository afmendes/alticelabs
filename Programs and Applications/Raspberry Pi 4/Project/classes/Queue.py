class Queue(object):
    """FIFO Logic"""
    def __init__(self, max_size: int = 1000):
        self.__item = []

    def enqueue(self, add):
        self.__item.insert(0, add)
        return True

    def dequeue(self):
        if not self.is_empty():
            return self.__item.pop()

    def is_empty(self):
        if not self.__item:
            return True
        return False
