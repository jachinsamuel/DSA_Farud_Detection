import unittest
from dsa.linear.stack import Stack, StackUsingLinkedList
from dsa.linear.queue import Queue, CircularQueue, PriorityQueue
from dsa.linear.deque import Deque
from dsa.linear.linked_list import SinglyLinkedList, DoublyLinkedList, CircularLinkedList
from dsa.searching_sorting.hash_table import HashTableChaining, HashTableOpenAddressing
from dsa.searching_sorting.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort
from dsa.searching_sorting.searching import sequential_search, binary_search_iterative, binary_search_recursive, interpolation_search
from dsa.trees.heap import MinHeap, MaxHeap
from dsa.trees.bst import BinarySearchTree
from dsa.trees.trie import Trie
from dsa.graphs.graph import TransactionGraph
from dsa.graphs.dfs_cycles import CycleDetectorDFS
from dsa.graphs.bfs_traversal import BFSDispersalAnalyzer
from dsa.graphs.dijkstra import SuspiciousPathFinder
from engine.fraud_detector import FraudDetectionEngine

class TestDSAFraudDetection(unittest.TestCase):

    def test_stack(self):
        s = Stack()
        s.push(10)
        s.push(20)
        self.assertEqual(s.peek(), 20)
        self.assertEqual(s.pop(), 20)
        self.assertEqual(s.pop(), 10)
        self.assertTrue(s.is_empty())
        s_ll = StackUsingLinkedList()
        s_ll.push('A')
        s_ll.push('B')
        self.assertEqual(s_ll.pop(), 'B')
        self.assertEqual(s_ll.pop(), 'A')

    def test_circular_queue(self):
        cq = CircularQueue(capacity=3)
        self.assertTrue(cq.is_empty())
        cq.enqueue('TX1')
        cq.enqueue('TX2')
        cq.enqueue('TX3')
        self.assertTrue(cq.is_full())
        self.assertEqual(cq.dequeue(), 'TX1')
        self.assertFalse(cq.is_full())
        cq.enqueue('TX4')
        self.assertEqual(cq.dequeue(), 'TX2')
        self.assertEqual(cq.dequeue(), 'TX3')
        self.assertEqual(cq.dequeue(), 'TX4')
        self.assertTrue(cq.is_empty())

    def test_deque(self):
        dq = Deque()
        dq.add_front(1)
        dq.add_rear(2)
        dq.add_front(0)
        self.assertEqual(dq.remove_front(), 0)
        self.assertEqual(dq.remove_rear(), 2)
        self.assertEqual(dq.remove_front(), 1)
        self.assertTrue(dq.is_empty())

    def test_linked_lists(self):
        sll = SinglyLinkedList()
        sll.insert_at_tail(10)
        sll.insert_at_head(5)
        self.assertEqual(sll.to_list(), [5, 10])
        self.assertTrue(sll.delete(10))
        self.assertEqual(sll.to_list(), [5])
        dll = DoublyLinkedList()
        dll.insert_at_tail('Event1')
        dll.insert_at_tail('Event2')
        self.assertEqual(dll.forward_traversal(), ['Event1', 'Event2'])
        self.assertEqual(dll.backward_traversal(), ['Event2', 'Event1'])

    def test_hash_tables(self):
        ht_chain = HashTableChaining(capacity=5)
        ht_chain.put('ACC-1', {'name': 'Alice'})
        ht_chain.put('ACC-2', {'name': 'Bob'})
        self.assertEqual(ht_chain.get('ACC-1')['name'], 'Alice')
        self.assertEqual(ht_chain.get('ACC-2')['name'], 'Bob')
        ht_open = HashTableOpenAddressing(capacity=5)
        ht_open.put('K1', 100)
        ht_open.put('K2', 200)
        self.assertEqual(ht_open.get('K1'), 100)
        self.assertEqual(ht_open.get('K2'), 200)

    def test_sorting(self):
        arr = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 45]
        expected = sorted(arr)
        self.assertEqual(bubble_sort(arr)[0], expected)
        self.assertEqual(selection_sort(arr)[0], expected)
        self.assertEqual(insertion_sort(arr)[0], expected)
        self.assertEqual(merge_sort(arr)[0], expected)

    def test_searching(self):
        arr = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        self.assertEqual(sequential_search(arr, 50)[0], 4)
        self.assertEqual(binary_search_iterative(arr, 50)[0], 4)
        self.assertEqual(binary_search_recursive(arr, 50)[0], 4)
        self.assertEqual(interpolation_search(arr, 50)[0], 4)

    def test_min_max_heap(self):
        min_h = MinHeap()
        for x in [50, 30, 20, 40, 10]:
            min_h.insert(x)
        extracted = [min_h.extract_min() for _ in range(5)]
        self.assertEqual(extracted, [10, 20, 30, 40, 50])
        max_h = MaxHeap()
        for x in [50, 30, 20, 40, 10]:
            max_h.insert(x)
        extracted_max = [max_h.extract_max() for _ in range(5)]
        self.assertEqual(extracted_max, [50, 40, 30, 20, 10])

    def test_bst_and_range_search(self):
        bst = BinarySearchTree()
        bst.insert(500, 'TX_500')
        bst.insert(200, 'TX_200')
        bst.insert(800, 'TX_800')
        bst.insert(350, 'TX_350')
        inorder = bst.inorder_traversal()
        self.assertEqual(inorder, [200, 350, 500, 800])
        range_results = bst.range_search(300, 700)
        self.assertEqual(sorted(range_results), ['TX_350', 'TX_500'])

    def test_trie(self):
        trie = Trie()
        trie.insert('ACC-101', 'Account 101')
        trie.insert('ACC-102', 'Account 102')
        trie.insert('BOB-SMITH', 'Bob')
        self.assertEqual(trie.search('ACC-101'), 'Account 101')
        results = trie.starts_with('ACC-')
        self.assertEqual(len(results), 2)

    def test_graph_and_fraud_algorithms(self):
        g = TransactionGraph()
        g.add_transaction('A', 'B', 1000, 1)
        g.add_transaction('B', 'C', 950, 2)
        g.add_transaction('C', 'A', 900, 3)
        detector = CycleDetectorDFS(g)
        cycles = detector.find_all_cycles()
        self.assertGreaterEqual(len(cycles), 1)
        self.assertEqual(cycles[0]['path'], ['A', 'B', 'C', 'A'])
        path_finder = SuspiciousPathFinder(g)
        res = path_finder.find_shortest_chain('A', 'C')
        self.assertTrue(res['found'])
        self.assertEqual(res['path'], ['A', 'B', 'C'])

    def test_end_to_end_engine(self):
        engine = FraudDetectionEngine()
        engine.load_from_json('data/transactions_dataset.json')
        cycles = engine.run_cycle_detection()
        self.assertTrue(any(('ACC-101' in c['accounts_involved'] for c in cycles)))
        smurfs = engine.run_smurfing_detection()
        self.assertTrue(any((s['primary_account'] == 'ACC-200' for s in smurfs)))
        mule_path = engine.trace_mule_chain('ACC-901', 'ACC-999')
        self.assertTrue(mule_path['found'])
        self.assertEqual(mule_path['path'], ['ACC-901', 'ACC-902', 'ACC-903', 'ACC-999'])
if __name__ == '__main__':
    unittest.main()
