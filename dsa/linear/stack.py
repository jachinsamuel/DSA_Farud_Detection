from dsa.linear.linked_list import SinglyLinkedList

class Stack:

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError('pop from empty stack')
        return self._items.pop()

    def peek(self):
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
        return f'Stack({self._items})'

class StackUsingLinkedList:

    def __init__(self):
        self._list = SinglyLinkedList()

    def push(self, item):
        self._list.insert_at_head(item)

    def pop(self):
        if self.is_empty():
            raise IndexError('pop from empty stack')
        top_data = self._list.head.data
        self._list.delete(lambda d: d == top_data)
        return top_data

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
