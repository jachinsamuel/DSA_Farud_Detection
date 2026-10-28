from dsa.linear.linked_list import SinglyLinkedList

class Edge:

    def __init__(self, src, dest, amount, timestamp, tx_id=None):
        self.src = src
        self.dest = dest
        self.amount = float(amount)
        self.timestamp = timestamp
        self.tx_id = tx_id or f'TX-{src}-{dest}-{timestamp}'

    def to_dict(self):
        return {'tx_id': self.tx_id, 'src': self.src, 'dest': self.dest, 'amount': self.amount, 'timestamp': self.timestamp}

    def __repr__(self):
        return f'Edge({self.src} -> {self.dest}, ${self.amount}, t={self.timestamp})'

class Vertex:

    def __init__(self, account_id, name='Unknown', risk_score=0.0, balance=10000.0, is_flagged=False):
        self.account_id = account_id
        self.name = name
        self.risk_score = risk_score
        self.balance = balance
        self.is_flagged = is_flagged
        self.edges = SinglyLinkedList()

    def add_edge(self, edge):
        self.edges.insert_at_tail(edge)

    def get_outgoing_edges(self):
        return self.edges.to_list()

    def out_degree(self):
        return self.edges.size()

    def to_dict(self):
        return {'account_id': self.account_id, 'name': self.name, 'risk_score': self.risk_score, 'balance': self.balance, 'is_flagged': self.is_flagged, 'out_degree': self.out_degree()}

    def __repr__(self):
        return f'Vertex({self.account_id}, {self.name}, Risk={self.risk_score})'

class TransactionGraph:

    def __init__(self):
        self.vertices = {}
        self.all_edges = []

    def add_vertex(self, account_id, name='Unknown', risk_score=0.0, balance=10000.0, is_flagged=False):
        if account_id not in self.vertices:
            self.vertices[account_id] = Vertex(account_id=account_id, name=name, risk_score=risk_score, balance=balance, is_flagged=is_flagged)
        return self.vertices[account_id]

    def add_transaction(self, src_id, dest_id, amount, timestamp, tx_id=None):
        if src_id not in self.vertices:
            self.add_vertex(src_id)
        if dest_id not in self.vertices:
            self.add_vertex(dest_id)
        edge = Edge(src_id, dest_id, amount, timestamp, tx_id)
        self.vertices[src_id].add_edge(edge)
        self.all_edges.append(edge)
        return edge

    def get_vertex(self, account_id):
        return self.vertices.get(account_id)

    def get_all_vertices(self):
        return list(self.vertices.values())

    def get_all_edges(self):
        return list(self.all_edges)

    def vertex_count(self):
        return len(self.vertices)

    def edge_count(self):
        return len(self.all_edges)

    def to_adjacency_matrix(self):
        node_ids = sorted(list(self.vertices.keys()))
        idx_map = {acc_id: i for i, acc_id in enumerate(node_ids)}
        n = len(node_ids)
        matrix = [[0.0] * n for _ in range(n)]
        for src_id, vertex in self.vertices.items():
            u = idx_map[src_id]
            for edge in vertex.get_outgoing_edges():
                v = idx_map[edge.dest]
                matrix[u][v] += edge.amount
        return (matrix, node_ids)

    def to_json_dict(self):
        nodes = []
        for v in self.vertices.values():
            nodes.append({'id': v.account_id, 'label': f'{v.account_id}\n({v.name})', 'name': v.name, 'risk_score': v.risk_score, 'balance': v.balance, 'is_flagged': v.is_flagged, 'out_degree': v.out_degree()})
        links = []
        for e in self.all_edges:
            links.append({'id': e.tx_id, 'source': e.src, 'target': e.dest, 'amount': e.amount, 'timestamp': e.timestamp})
        return {'nodes': nodes, 'links': links}
