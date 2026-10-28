from dsa.linear.queue import Queue

class BFSDispersalAnalyzer:

    def __init__(self, graph):
        self.graph = graph

    def trace_fund_flow(self, start_account_id, max_hops=3):
        if start_account_id not in self.graph.vertices:
            return None
        visited = {start_account_id: 0}
        q = Queue()
        q.enqueue((start_account_id, 0))
        levels = {}
        edges_traversed = []
        while not q.is_empty():
            curr_node, current_hop = q.dequeue()
            if current_hop not in levels:
                levels[current_hop] = []
            levels[current_hop].append(curr_node)
            if current_hop < max_hops:
                vertex = self.graph.get_vertex(curr_node)
                if vertex:
                    for edge in vertex.get_outgoing_edges():
                        dest = edge.dest
                        edges_traversed.append(edge.to_dict())
                        if dest not in visited:
                            visited[dest] = current_hop + 1
                            q.enqueue((dest, current_hop + 1))
        return {'root_account': start_account_id, 'max_hops': max_hops, 'total_reached_accounts': len(visited), 'levels': levels, 'edges_traversed': edges_traversed}

    def detect_smurfing(self, fan_out_threshold=3, min_total_amount=1000.0):
        suspicious_patterns = []
        for acc_id, vertex in self.graph.vertices.items():
            outgoing = vertex.get_outgoing_edges()
            unique_recipients = set((e.dest for e in outgoing))
            total_sent = sum((e.amount for e in outgoing))
            if len(unique_recipients) >= fan_out_threshold and total_sent >= min_total_amount:
                suspicious_patterns.append({'pattern_type': 'Smurfing (Fan-Out / Structuring)', 'primary_account': acc_id, 'target_accounts': list(unique_recipients), 'recipient_count': len(unique_recipients), 'total_amount': round(total_sent, 2), 'severity': 'HIGH', 'description': f'Account {acc_id} rapidly dispersed ${total_sent:,.2f} to {len(unique_recipients)} distinct recipients.'})
        inbound_map = {}
        for edge in self.graph.all_edges:
            if edge.dest not in inbound_map:
                inbound_map[edge.dest] = []
            inbound_map[edge.dest].append((edge.src, edge.amount))
        for dest_id, inbound_txs in inbound_map.items():
            unique_senders = set((src for src, _ in inbound_txs))
            total_received = sum((amt for _, amt in inbound_txs))
            if len(unique_senders) >= fan_out_threshold and total_received >= min_total_amount:
                suspicious_patterns.append({'pattern_type': 'Mule Funneling (Fan-In)', 'primary_account': dest_id, 'target_accounts': list(unique_senders), 'sender_count': len(unique_senders), 'total_amount': round(total_received, 2), 'severity': 'HIGH', 'description': f'Collection Account {dest_id} funneled ${total_received:,.2f} from {len(unique_senders)} distinct source accounts.'})
        return suspicious_patterns
