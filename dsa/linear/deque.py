class Deque:

    def __init__(self):
        self._items = []

    def add_front(self, item):
        self._items.insert(0, item)

    def add_rear(self, item):
        self._items.append(item)

    def remove_front(self):
        if self.is_empty():
            raise IndexError('remove_front from empty deque')
        return self._items.pop(0)

    def remove_rear(self):
        if self.is_empty():
            raise IndexError('remove_rear from empty deque')
        return self._items.pop()

    def peek_front(self):
        if self.is_empty():
            return None
        return self._items[0]

    def peek_rear(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f'Deque({self._items})'
