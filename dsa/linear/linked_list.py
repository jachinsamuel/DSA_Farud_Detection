class SinglyNode:

    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f'SinglyNode({self.data})'

class SinglyLinkedList:

    def __init__(self):
        self.head = None
        self._size = 0

    def insert_at_head(self, data):
        new_node = SinglyNode(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at_tail(self, data):
        new_node = SinglyNode(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def delete(self, key_or_predicate):
        curr = self.head
        prev = None
        while curr:
            is_match = key_or_predicate(curr.data) if callable(key_or_predicate) else curr.data == key_or_predicate
            if is_match:
                if prev is None:
                    self.head = curr.next
                else:
                    prev.next = curr.next
                self._size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def search(self, key_or_predicate):
        curr = self.head
        while curr:
            is_match = key_or_predicate(curr.data) if callable(key_or_predicate) else curr.data == key_or_predicate
            if is_match:
                return curr.data
            curr = curr.next
        return None

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def size(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    def __len__(self):
        return self._size

    def __repr__(self):
        items = ' -> '.join((str(d) for d in self.to_list()))
        return f'[{items}]' if items else '[]'

class DoublyNode:

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f'DoublyNode({self.data})'

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def insert_at_head(self, data):
        new_node = DoublyNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_at_tail(self, data):
        new_node = DoublyNode(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def forward_traversal(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def backward_traversal(self):
        result = []
        curr = self.tail
        while curr:
            result.append(curr.data)
            curr = curr.prev
        return result

    def size(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self._size

class CircularLinkedList:

    def __init__(self):
        self.head = None
        self._size = 0

    def insert(self, data):
        new_node = SinglyNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            curr = self.head
            while curr.next != self.head:
                curr = curr.next
            curr.next = new_node
            new_node.next = self.head
        self._size += 1

    def to_list(self):
        if not self.head:
            return []
        result = []
        curr = self.head
        while True:
            result.append(curr.data)
            curr = curr.next
            if curr == self.head:
                break
        return result

    def size(self):
        return self._size
