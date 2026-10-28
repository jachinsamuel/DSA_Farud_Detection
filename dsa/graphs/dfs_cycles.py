from dsa.linear.stack import Stack

class CycleDetectorDFS:
    WHITE = 0
    GRAY = 1
    BLACK = 2

    def __init__(self, graph):
        self.graph = graph

    def find_all_cycles(self, max_cycle_length=8):
        visited = {acc_id: self.WHITE for acc_id in self.graph.vertices}
        current_stack = Stack()
        detected_cycles = []
        seen_cycles_canonical = set()

        def _dfs(u):
            visited[u] = self.GRAY
            current_stack.push(u)
            vertex_u = self.graph.get_vertex(u)
            if vertex_u:
                for edge in vertex_u.get_outgoing_edges():
                    v = edge.dest
                    if visited.get(v, self.WHITE) == self.GRAY:
                        stack_items = current_stack.to_list()
                        if v in stack_items:
                            cycle_start_idx = stack_items.index(v)
                            cycle_nodes = stack_items[cycle_start_idx:] + [v]
                            if 2 <= len(cycle_nodes) - 1 <= max_cycle_length:
                                loop = cycle_nodes[:-1]
                                min_idx = loop.index(min(loop))
                                canonical = tuple(loop[min_idx:] + loop[:min_idx])
                                if canonical not in seen_cycles_canonical:
                                    seen_cycles_canonical.add(canonical)
                                    cycle_info = self._analyze_cycle(cycle_nodes)
                                    detected_cycles.append(cycle_info)
                    elif visited.get(v, self.WHITE) == self.WHITE:
                        _dfs(v)
            current_stack.pop()
            visited[u] = self.BLACK
        for node in list(self.graph.vertices.keys()):
            if visited[node] == self.WHITE:
                _dfs(node)
        return detected_cycles

    def _analyze_cycle(self, cycle_nodes):
        ring_edges = []
        total_volume = 0.0
        min_amount = float('inf')
        timestamps = []
        for i in range(len(cycle_nodes) - 1):
            src = cycle_nodes[i]
            dest = cycle_nodes[i + 1]
            src_v = self.graph.get_vertex(src)
            if src_v:
                for edge in src_v.get_outgoing_edges():
                    if edge.dest == dest:
                        ring_edges.append(edge.to_dict())
                        total_volume += edge.amount
                        min_amount = min(min_amount, edge.amount)
                        timestamps.append(edge.timestamp)
                        break
        risk_score = 95.0 if len(cycle_nodes) <= 5 else 80.0
        return {'cycle_id': f"RING-{'-'.join(cycle_nodes[:4])}", 'type': 'Circular Money Laundering (Round-Tripping)', 'path': cycle_nodes, 'hop_count': len(cycle_nodes) - 1, 'accounts_involved': list(dict.fromkeys(cycle_nodes[:-1])), 'total_volume': round(total_volume, 2), 'retained_volume': round(min_amount if min_amount != float('inf') else 0.0, 2), 'edges': ring_edges, 'risk_score': risk_score, 'severity': 'CRITICAL' if risk_score >= 90 else 'HIGH'}
