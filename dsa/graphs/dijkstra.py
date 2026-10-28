from dsa.trees.heap import MinHeap

class SuspiciousPathFinder:

    def __init__(self, graph):
        self.graph = graph

    def find_shortest_chain(self, source_id, target_id, weight_mode='hops'):
        if source_id not in self.graph.vertices or target_id not in self.graph.vertices:
            return {'found': False, 'error': 'Source or target account not found in graph'}
        distances = {v: float('inf') for v in self.graph.vertices}
        previous = {v: None for v in self.graph.vertices}
        edge_used = {v: None for v in self.graph.vertices}
        distances[source_id] = 0.0
        pq = MinHeap(key_func=lambda entry: entry[0])
        pq.insert((0.0, source_id))
        visited = set()
        while not pq.is_empty():
            curr_dist, u = pq.extract_min()
            if u in visited:
                continue
            visited.add(u)
            if u == target_id:
                break
            vertex = self.graph.get_vertex(u)
            if not vertex:
                continue
            for edge in vertex.get_outgoing_edges():
                v = edge.dest
                if v in visited:
                    continue
                if weight_mode == 'friction':
                    weight = 10000.0 / max(edge.amount, 1.0)
                else:
                    weight = 1.0
                alt_distance = curr_dist + weight
                if alt_distance < distances[v]:
                    distances[v] = alt_distance
                    previous[v] = u
                    edge_used[v] = edge
                    pq.insert((alt_distance, v))
        if distances[target_id] == float('inf'):
            return {'found': False, 'source': source_id, 'target': target_id, 'message': f'No transaction path connects {source_id} to {target_id}'}
        path = []
        tx_chain = []
        curr = target_id
        while curr is not None:
            path.append(curr)
            if edge_used[curr] is not None:
                tx_chain.append(edge_used[curr].to_dict())
            curr = previous[curr]
        path.reverse()
        tx_chain.reverse()
        return {'found': True, 'source': source_id, 'target': target_id, 'path': path, 'hop_count': len(path) - 1, 'total_cost': round(distances[target_id], 4), 'transactions': tx_chain, 'severity': 'CRITICAL' if len(path) - 1 <= 3 else 'MEDIUM', 'description': f'Detected suspicious mule chain of {len(path) - 1} hops from {source_id} to {target_id}.'}
