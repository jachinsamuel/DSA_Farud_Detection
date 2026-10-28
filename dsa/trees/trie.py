class TrieNode:

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.payload = None

    def __repr__(self):
        return f'TrieNode(is_end={self.is_end_of_word})'

class Trie:

    def __init__(self):
        self.root = TrieNode()
        self._size = 0

    def insert(self, word, payload=None):
        curr = self.root
        word_clean = str(word).strip().upper()
        for char in word_clean:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        if not curr.is_end_of_word:
            self._size += 1
        curr.is_end_of_word = True
        curr.payload = payload

    def search(self, word):
        curr = self.root
        word_clean = str(word).strip().upper()
        for char in word_clean:
            if char not in curr.children:
                return None
            curr = curr.children[char]
        return curr.payload if curr.is_end_of_word else None

    def starts_with(self, prefix, limit=10):
        curr = self.root
        prefix_clean = str(prefix).strip().upper()
        for char in prefix_clean:
            if char not in curr.children:
                return []
            curr = curr.children[char]
        results = []

        def _dfs(node, current_str):
            if len(results) >= limit:
                return
            if node.is_end_of_word:
                results.append({'word': current_str, 'payload': node.payload})
            for char in sorted(node.children.keys()):
                _dfs(node.children[char], current_str + char)
        _dfs(curr, prefix_clean)
        return results

    def size(self):
        return self._size
