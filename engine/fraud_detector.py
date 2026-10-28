import json
import time
from dsa.linear.queue import CircularQueue
from dsa.linear.deque import Deque
from dsa.linear.linked_list import DoublyLinkedList
from dsa.trees.heap import HeapPriorityQueue, MaxHeap
from dsa.trees.trie import Trie
from dsa.trees.bst import BinarySearchTree
from dsa.searching_sorting.hash_table import HashTableChaining
from dsa.searching_sorting.sorting import merge_sort
from dsa.searching_sorting.searching import binary_search_iterative, sequential_search
from dsa.graphs.graph import TransactionGraph
from dsa.graphs.dfs_cycles import CycleDetectorDFS
from dsa.graphs.bfs_traversal import BFSDispersalAnalyzer
from dsa.graphs.dijkstra import SuspiciousPathFinder

class FraudDetectionEngine:

    def __init__(self, buffer_capacity=10):
        self.graph = TransactionGraph()
        self.ingestion_buffer = CircularQueue(capacity=buffer_capacity)
        self.velocity_deque = Deque()
        self.alert_queue = HeapPriorityQueue()
        self.audit_ledger = DoublyLinkedList()
        self.account_trie = Trie()
        self.amount_bst = BinarySearchTree()
        self.top_risk_heap = MaxHeap(key_func=lambda alert: alert['risk_score'])
        self.account_table = HashTableChaining(capacity=31)
        self.cycle_detector = CycleDetectorDFS(self.graph)
        self.dispersal_analyzer = BFSDispersalAnalyzer(self.graph)
        self.path_finder = SuspiciousPathFinder(self.graph)

    def load_from_json(self, json_filepath):
        with open(json_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for acc in data.get('accounts', []):
            self.register_account(account_id=acc['account_id'], name=acc.get('name', 'Unknown'), risk_score=acc.get('risk_score', 0.0), balance=acc.get('balance', 10000.0), is_flagged=acc.get('is_flagged', False))
        for tx in data.get('transactions', []):
            self.process_transaction(src_id=tx['src'], dest_id=tx['dest'], amount=tx['amount'], timestamp=tx.get('timestamp', int(time.time())), tx_id=tx.get('tx_id'))

    def register_account(self, account_id, name='Unknown', risk_score=0.0, balance=10000.0, is_flagged=False):
        acc_dict = {'account_id': account_id, 'name': name, 'risk_score': risk_score, 'balance': balance, 'is_flagged': is_flagged}
        self.graph.add_vertex(account_id, name, risk_score, balance, is_flagged)
        self.account_table.put(account_id, acc_dict)
        self.account_trie.insert(account_id, acc_dict)
        self.account_trie.insert(name, acc_dict)
        return acc_dict

    def process_transaction(self, src_id, dest_id, amount, timestamp=None, tx_id=None):
        if timestamp is None:
            timestamp = int(time.time())
        tx_payload = {'tx_id': tx_id or f'TX-{src_id}-{dest_id}-{timestamp}', 'src': src_id, 'dest': dest_id, 'amount': float(amount), 'timestamp': timestamp}
        try:
            self.ingestion_buffer.enqueue(tx_payload)
        except OverflowError:
            self.ingestion_buffer.dequeue()
            self.ingestion_buffer.enqueue(tx_payload)
        edge = self.graph.add_transaction(src_id, dest_id, amount, timestamp, tx_payload['tx_id'])
        self.amount_bst.insert(float(amount), tx_payload)
        self.audit_ledger.insert_at_tail(tx_payload)
        velocity_alert = self._check_velocity(src_id, timestamp)
        if velocity_alert:
            self.alert_queue.push(velocity_alert, priority=1)
            self.top_risk_heap.insert(velocity_alert)
        return tx_payload

    def _check_velocity(self, src_id, current_time, window_seconds=120, threshold=4):
        self.velocity_deque.add_rear((src_id, current_time))
        while not self.velocity_deque.is_empty():
            oldest_src, oldest_time = self.velocity_deque.peek_front()
            if current_time - oldest_time > window_seconds:
                self.velocity_deque.remove_front()
            else:
                break
        active_txs = self.velocity_deque.to_list()
        count = sum((1 for acc, _ in active_txs if acc == src_id))
        if count >= threshold:
            return {'alert_id': f'VELOCITY-{src_id}-{current_time}', 'type': 'High-Frequency Transaction Velocity Burst', 'account_id': src_id, 'count': count, 'window_seconds': window_seconds, 'risk_score': 92.0, 'severity': 'CRITICAL', 'timestamp': current_time, 'description': f'Account {src_id} executed {count} transactions within {window_seconds}s window.'}
        return None

    def run_cycle_detection(self):
        cycles = self.cycle_detector.find_all_cycles()
        for c in cycles:
            self.alert_queue.push(c, priority=1)
            self.top_risk_heap.insert(c)
        return cycles

    def run_smurfing_detection(self):
        patterns = self.dispersal_analyzer.detect_smurfing()
        for p in patterns:
            alert = {'alert_id': f"SMURF-{p['primary_account']}", 'type': p['pattern_type'], 'risk_score': 88.0, 'severity': p['severity'], 'details': p}
            self.alert_queue.push(alert, priority=2)
        return patterns

    def trace_mule_chain(self, source_id, target_id):
        return self.path_finder.find_shortest_chain(source_id, target_id)

    def trace_fund_flow_bfs(self, start_id, max_hops=3):
        return self.dispersal_analyzer.trace_fund_flow(start_id, max_hops=max_hops)

    def filter_transactions_by_amount_range(self, min_amt, max_amt):
        return self.amount_bst.range_search(min_amt, max_amt)

    def search_account_autocomplete(self, prefix):
        return self.account_trie.starts_with(prefix)

    def get_account_instant(self, account_id):
        return self.account_table.get(account_id)

    def get_sorted_transactions_by_amount(self):
        all_txs = self.graph.get_all_edges()
        dicts = [e.to_dict() for e in all_txs]
        sorted_txs, comparisons = merge_sort(dicts, key=lambda x: x['amount'])
        return (sorted_txs, comparisons)
