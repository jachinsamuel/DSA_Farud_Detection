from dsa.linear.linked_list import SinglyLinkedList

class HashEntry:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'({self.key}: {self.value})'

class HashTableChaining:

    def __init__(self, capacity=17):
        self.capacity = capacity
        self.buckets = [SinglyLinkedList() for _ in range(capacity)]
        self._size = 0

    def _hash(self, key):
        hash_val = 0
        p = 31
        for char in str(key):
            hash_val = (hash_val * p + ord(char)) % self.capacity
        return hash_val

    def put(self, key, value):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        curr = bucket.head
        while curr:
            entry = curr.data
            if entry.key == key:
                entry.value = value
                return
            curr = curr.next
        bucket.insert_at_head(HashEntry(key, value))
        self._size += 1
        if self._size / self.capacity > 0.75:
            self._rehash(self.capacity * 2 + 1)

    def get(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        curr = bucket.head
        while curr:
            if curr.data.key == key:
                return curr.data.value
            curr = curr.next
        return None

    def delete(self, key):
        idx = self._hash(key)
        bucket = self.buckets[idx]
        deleted = bucket.delete(lambda entry: entry.key == key)
        if deleted:
            self._size -= 1
        return deleted

    def contains(self, key):
        return self.get(key) is not None

    def _rehash(self, new_capacity):
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [SinglyLinkedList() for _ in range(new_capacity)]
        self._size = 0
        for b in old_buckets:
            curr = b.head
            while curr:
                self.put(curr.data.key, curr.data.value)
                curr = curr.next

    def keys(self):
        result = []
        for b in self.buckets:
            curr = b.head
            while curr:
                result.append(curr.data.key)
                curr = curr.next
        return result

    def values(self):
        result = []
        for b in self.buckets:
            curr = b.head
            while curr:
                result.append(curr.data.value)
                curr = curr.next
        return result

    def size(self):
        return self._size

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key, value):
        self.put(key, value)

class HashTableOpenAddressing:

    def __init__(self, capacity=19):
        self.capacity = capacity
        self.table = [None] * capacity
        self._size = 0
        self._DELETED = object()

    def _hash(self, key):
        hash_val = 0
        for char in str(key):
            hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val

    def put(self, key, value):
        if (self._size + 1) / self.capacity > 0.7:
            self._rehash(self.capacity * 2 + 1)
        idx = self._hash(key)
        first_deleted = None
        for i in range(self.capacity):
            probe_idx = (idx + i) % self.capacity
            slot = self.table[probe_idx]
            if slot is None:
                target_idx = first_deleted if first_deleted is not None else probe_idx
                self.table[target_idx] = HashEntry(key, value)
                self._size += 1
                return
            elif slot is self._DELETED:
                if first_deleted is None:
                    first_deleted = probe_idx
            elif slot.key == key:
                slot.value = value
                return
        raise OverflowError('Hash table full')

    def get(self, key):
        idx = self._hash(key)
        for i in range(self.capacity):
            probe_idx = (idx + i) % self.capacity
            slot = self.table[probe_idx]
            if slot is None:
                return None
            if slot is not self._DELETED and slot.key == key:
                return slot.value
        return None

    def delete(self, key):
        idx = self._hash(key)
        for i in range(self.capacity):
            probe_idx = (idx + i) % self.capacity
            slot = self.table[probe_idx]
            if slot is None:
                return False
            if slot is not self._DELETED and slot.key == key:
                self.table[probe_idx] = self._DELETED
                self._size -= 1
                return True
        return False

    def _rehash(self, new_capacity):
        old_table = self.table
        self.capacity = new_capacity
        self.table = [None] * new_capacity
        self._size = 0
        for slot in old_table:
            if slot is not None and slot is not self._DELETED:
                self.put(slot.key, slot.value)
