import os
from flask import Flask, jsonify, request, render_template
from engine.fraud_detector import FraudDetectionEngine
from dsa.searching_sorting.benchmark import benchmark_sorting, benchmark_searching
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'web', 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'web', 'static'))
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'transactions_dataset.json')
engine = FraudDetectionEngine(buffer_capacity=10)
if os.path.exists(DATA_PATH):
    engine.load_from_json(DATA_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph', methods=['GET'])
def get_graph():
    return jsonify(engine.graph.to_json_dict())

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    nodes = [v.to_dict() for v in engine.graph.get_all_vertices()]
    return jsonify(nodes)

@app.route('/api/detect/cycles', methods=['GET'])
def detect_cycles():
    cycles = engine.run_cycle_detection()
    return jsonify({'success': True, 'count': len(cycles), 'cycles': cycles})

@app.route('/api/detect/smurfing', methods=['GET'])
def detect_smurfing():
    patterns = engine.run_smurfing_detection()
    return jsonify({'success': True, 'count': len(patterns), 'patterns': patterns})

@app.route('/api/detect/shortest-path', methods=['POST'])
def shortest_path():
    data = request.get_json() or {}
    source = data.get('source')
    target = data.get('target')
    weight_mode = data.get('weight_mode', 'hops')
    if not source or not target:
        return (jsonify({'success': False, 'error': 'Source and target account IDs are required'}), 400)
    result = engine.trace_mule_chain(source, target)
    return jsonify({'success': True, 'result': result})

@app.route('/api/trace/bfs', methods=['GET'])
def trace_bfs():
    start = request.args.get('account_id')
    hops = int(request.args.get('hops', 3))
    if not start:
        return (jsonify({'success': False, 'error': 'Account ID required'}), 400)
    result = engine.trace_fund_flow_bfs(start, max_hops=hops)
    return jsonify({'success': True, 'result': result})

@app.route('/api/search/trie', methods=['GET'])
def search_trie():
    query = request.args.get('q', '')
    matches = engine.search_account_autocomplete(query)
    return jsonify({'success': True, 'query': query, 'matches': matches})

@app.route('/api/search/account', methods=['GET'])
def search_account():
    account_id = request.args.get('id', '')
    acc = engine.get_account_instant(account_id)
    if acc:
        return jsonify({'success': True, 'found': True, 'account': acc})
    return (jsonify({'success': True, 'found': False, 'message': 'Account not found in Hash Table'}), 404)

@app.route('/api/filter/bst', methods=['GET'])
def filter_bst():
    min_amt = float(request.args.get('min', 0.0))
    max_amt = float(request.args.get('max', 1000000.0))
    transactions = engine.filter_transactions_by_amount_range(min_amt, max_amt)
    return jsonify({'success': True, 'min': min_amt, 'max': max_amt, 'count': len(transactions), 'transactions': transactions, 'inorder_sample': engine.amount_bst.inorder_traversal()[:15]})

@app.route('/api/transaction/create', methods=['POST'])
def create_transaction():
    data = request.get_json() or {}
    src = data.get('src')
    dest = data.get('dest')
    amount = float(data.get('amount', 0.0))
    if not src or not dest or amount <= 0:
        return (jsonify({'success': False, 'error': 'Invalid source, dest or amount'}), 400)
    tx = engine.process_transaction(src, dest, amount)
    buffer_state = engine.ingestion_buffer.get_buffer_state()
    return jsonify({'success': True, 'transaction': tx, 'buffer_state': buffer_state, 'alerts_count': engine.alert_queue.size()})

@app.route('/api/buffer/state', methods=['GET'])
def get_buffer_state():
    return jsonify({'success': True, 'buffer': engine.ingestion_buffer.get_buffer_state(), 'deque_size': engine.velocity_deque.size(), 'ledger_size': engine.audit_ledger.size()})

@app.route('/api/matrix', methods=['GET'])
def get_matrix():
    matrix, nodes = engine.graph.to_adjacency_matrix()
    return jsonify({'success': True, 'nodes': nodes, 'matrix': matrix})

@app.route('/api/benchmark/sorting', methods=['GET'])
def get_sorting_benchmark():
    results = benchmark_sorting(sizes=(50, 100, 200, 400, 800))
    return jsonify({'success': True, 'data': results})

@app.route('/api/benchmark/searching', methods=['GET'])
def get_searching_benchmark():
    results = benchmark_searching(sizes=(200, 1000, 5000, 10000, 20000))
    return jsonify({'success': True, 'data': results})
@app.route('/favicon.ico')
def favicon():
    return ('', 204)

@app.route('/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict_fraud():
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    src = data.get('src') or data.get('source') or data.get('sender') or data.get('account_id')
    dest = data.get('dest') or data.get('target') or data.get('receiver')
    try:
        amount = float(data.get('amount', 0.0))
    except (ValueError, TypeError):
        amount = 0.0

    risk_factors = []
    risk_score = 10.0

    src_acc = engine.get_account_instant(src) if src else None
    dest_acc = engine.get_account_instant(dest) if dest else None

    if src_acc and (src_acc.get('is_flagged') or src_acc.get('risk_score', 0) >= 80):
        risk_score += 45.0
        risk_factors.append(f"Origin account {src} is flagged or has elevated risk ({src_acc.get('risk_score')}%).")

    if dest_acc and (dest_acc.get('is_flagged') or dest_acc.get('risk_score', 0) >= 80):
        risk_score += 45.0
        risk_factors.append(f"Destination account {dest} is flagged or has elevated risk ({dest_acc.get('risk_score')}%).")

    if amount >= 50000.0:
        risk_score += 25.0
        risk_factors.append(f"High-value transaction amount (${amount:,.2f}) exceeding threshold.")

    if src and dest:
        chain = engine.trace_mule_chain(src, dest)
        if chain.get('found') and chain.get('hop_count', 99) <= 4:
            risk_score += 20.0
            risk_factors.append(f"Connected to known money mule chain ({chain.get('hop_count')} hops).")

    is_fraud = risk_score >= 60.0 or (src_acc and src_acc.get('is_flagged')) or (dest_acc and dest_acc.get('is_flagged'))

    return jsonify({
        'is_fraud': is_fraud,
        'prediction': 'FRAUD' if is_fraud else 'LEGITIMATE',
        'risk_score': min(100.0, round(risk_score, 1)),
        'decision': 'BLOCK_AND_FLAG' if is_fraud else 'APPROVE',
        'risk_factors': risk_factors,
        'source': src,
        'destination': dest,
        'amount': amount
    })

if __name__ == '__main__':
    print('=' * 65)
    print(' BANK FRAUD DETECTION SYSTEM (DSA MICROPROJECT - CO1 TO CO5)')
    print(' Server starting on http://127.0.0.1:5000')
    print('=' * 65)
    app.run(debug=True, host='127.0.0.1', port=5000)
