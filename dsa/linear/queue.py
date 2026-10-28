from dsa.linear.linked_list import SinglyLinkedList

class Queue:

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError('dequeue from empty queue')
        return self._items.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f'Queue({self._items})'

class QueueUsingLinkedList:

    def __init__(self):
        self._list = SinglyLinkedList()

    def enqueue(self, item):
        self._list.insert_at_tail(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError('dequeue from empty queue')
        front_data = self._list.head.data
        self._list.delete(lambda d: d == front_data)
        return front_data

    def peek(self):
        if self.is_empty():
            return None
        return self._list.head.data

    def is_empty(self):
        return self._list.is_empty()

    def size(self):
        return self._list.size()

    def to_list(self):
        return self._list.to_list()

class CircularQueue:

    def __init__(self, capacity=10):
        if capacity <= 0:
            raise ValueError('Capacity must be positive')
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front = -1
        self.rear = -1
        self._size = 0

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def is_empty(self):
        return self.front == -1

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError('Circular Queue is full')
        if self.front == -1:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self._size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            raise IndexError('Circular Queue is empty')
        data = self.queue[self.front]
        self.queue[self.front] = None
        self._size -= 1
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        return data

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[self.front]

    def size(self):
        return self._size

    def to_list(self):
        if self.is_empty():
            return []
        items = []
        idx = self.front
        while True:
            items.append(self.queue[idx])
            if idx == self.rear:
                break
            idx = (idx + 1) % self.capacity
        return items

    def get_buffer_state(self):
        return {'slots': [item if item is not None else None for item in self.queue], 'front': self.front, 'rear': self.rear, 'capacity': self.capacity, 'size': self._size, 'is_full': self.is_full(), 'is_empty': self.is_empty()}

class PriorityQueue:

    def __init__(self):
        self._items = []

    def enqueue(self, item, priority):
        entry = (priority, item)
        inserted = False
        for i in range(len(self._items)):
            if priority < self._items[i][0]:
                self._items.insert(i, entry)
                inserted = True
                break
        if not inserted:
            self._items.append(entry)

    def dequeue(self):
        if self.is_empty():
            raise IndexError('Priority Queue is empty')
        priority, item = self._items.pop(0)
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._items[0][1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return [item for _, item in self._items]
