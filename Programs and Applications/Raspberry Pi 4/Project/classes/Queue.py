# simple queue class with FIFO logic
class Queue(object):
    """FIFO Logic"""
    def __init__(self, max_size: int = 1000):
        self.__item = []

    # adds a new item on the start of the queue
    def enqueue(self, add):
        self.__item.insert(0, add)
        return True

    # removes the last items of the queue
    def dequeue(self):
        if not self.is_empty():
            return self.__item.pop()

    # checks if the queue is empty and return True if it is, else returns False
    def is_empty(self):
        if not self.__item:
            return True
        return False
