class MinHeap:

    def __init__(self, key_func=lambda x: x):
        self.heap = []
        self.key_func = key_func

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _has_left(self, i):
        return self._left_child(i) < len(self.heap)

    def _has_right(self, i):
        return self._right_child(i) < len(self.heap)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = (self.heap[j], self.heap[i])

    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, i):
        parent = self._parent(i)
        while i > 0 and self.key_func(self.heap[i]) < self.key_func(self.heap[parent]):
            self._swap(i, parent)
            i = parent
            parent = self._parent(i)

    def extract_min(self):
        if self.is_empty():
            raise IndexError('extract_min from empty heap')
        if len(self.heap) == 1:
            return self.heap.pop()
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_val

    def _sift_down(self, i):
        while self._has_left(i):
            smallest = self._left_child(i)
            if self._has_right(i) and self.key_func(self.heap[self._right_child(i)]) < self.key_func(self.heap[smallest]):
                smallest = self._right_child(i)
            if self.key_func(self.heap[smallest]) < self.key_func(self.heap[i]):
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def __len__(self):
        return len(self.heap)

class MaxHeap:

    def __init__(self, key_func=lambda x: x):
        self.heap = []
        self.key_func = key_func

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = (self.heap[j], self.heap[i])

    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, i):
        parent = self._parent(i)
        while i > 0 and self.key_func(self.heap[i]) > self.key_func(self.heap[parent]):
            self._swap(i, parent)
            i = parent
            parent = self._parent(i)

    def extract_max(self):
        if self.is_empty():
            raise IndexError('extract_max from empty heap')
        if len(self.heap) == 1:
            return self.heap.pop()
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return max_val

    def _sift_down(self, i):
        n = len(self.heap)
        while 2 * i + 1 < n:
            largest = 2 * i + 1
            right = 2 * i + 2
            if right < n and self.key_func(self.heap[right]) > self.key_func(self.heap[largest]):
                largest = right
            if self.key_func(self.heap[largest]) > self.key_func(self.heap[i]):
                self._swap(i, largest)
                i = largest
            else:
                break

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

class HeapPriorityQueue:

    def __init__(self):
        self.min_heap = MinHeap(key_func=lambda entry: entry[0])

    def push(self, item, priority):
        self.min_heap.insert((priority, item))

    def pop(self):
        if self.min_heap.is_empty():
            raise IndexError('pop from empty priority queue')
        return self.min_heap.extract_min()[1]

    def is_empty(self):
        return self.min_heap.is_empty()

    def size(self):
        return self.min_heap.size()
