class BSTNode:

    def __init__(self, key, data=None):
        self.key = key
        self.data = data or []
        self.left = None
        self.right = None
        self.height = 1

    def __repr__(self):
        return f'BSTNode({self.key})'

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self._size = 0

    def insert(self, key, item):

        def _insert(node, k, val):
            if node is None:
                self._size += 1
                return BSTNode(k, [val])
            if k == node.key:
                node.data.append(val)
                self._size += 1
                return node
            elif k < node.key:
                node.left = _insert(node.left, k, val)
            else:
                node.right = _insert(node.right, k, val)
            return node
        self.root = _insert(self.root, key, item)

    def search(self, key):
        curr = self.root
        while curr:
            if curr.key == key:
                return curr.data
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return []

    def delete(self, key):

        def _min_value_node(node):
            current = node
            while current.left is not None:
                current = current.left
            return current

        def _delete(node, k):
            if node is None:
                return node
            if k < node.key:
                node.left = _delete(node.left, k)
            elif k > node.key:
                node.right = _delete(node.right, k)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                temp = _min_value_node(node.right)
                node.key = temp.key
                node.data = temp.data
                node.right = _delete(node.right, temp.key)
            return node
        self.root = _delete(self.root, key)

    def range_search(self, min_val, max_val):
        results = []

        def _range(node):
            if not node:
                return
            if node.key > min_val:
                _range(node.left)
            if min_val <= node.key <= max_val:
                results.extend(node.data)
            if node.key < max_val:
                _range(node.right)
        _range(self.root)
        return results

    def inorder_traversal(self):
        res = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

    def preorder_traversal(self):
        res = []

        def _preorder(node):
            if node:
                res.append(node.key)
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        return res

    def postorder_traversal(self):
        res = []

        def _postorder(node):
            if node:
                _postorder(node.left)
                _postorder(node.right)
                res.append(node.key)
        _postorder(self.root)
        return res

    def size(self):
        return self._size

    def to_tree_hierarchy(self):

        def _build(node):
            if not node:
                return None
            return {'key': node.key, 'count': len(node.data), 'left': _build(node.left), 'right': _build(node.right)}
        return _build(self.root)

class AVLTree(BinarySearchTree):

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def insert_balanced(self, key, item):

        def _insert(node, k, val):
            if not node:
                return BSTNode(k, [val])
            if k < node.key:
                node.left = _insert(node.left, k, val)
            elif k > node.key:
                node.right = _insert(node.right, k, val)
            else:
                node.data.append(val)
                return node
            node.height = 1 + max(self._height(node.left), self._height(node.right))
            balance = self._balance_factor(node)
            if balance > 1 and k < node.left.key:
                return self._right_rotate(node)
            if balance < -1 and k > node.right.key:
                return self._left_rotate(node)
            if balance > 1 and k > node.left.key:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
            if balance < -1 and k < node.right.key:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)
            return node
        self.root = _insert(self.root, key, item)
        self._size += 1
