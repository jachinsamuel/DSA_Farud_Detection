import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

def test_endpoints():
    client = app.test_client()
    r = client.get('/')
    assert r.status_code == 200, f'Index failed: {r.status_code}'
    assert b'Fraud Detection System' in r.data
    print('[OK] Index HTML endpoint OK')
    r = client.get('/api/graph')
    assert r.status_code == 200
    data = r.get_json()
    assert 'nodes' in data and 'links' in data
    print(f"[OK] Graph API OK: {len(data['nodes'])} nodes, {len(data['links'])} edges")
    r = client.get('/api/detect/cycles')
    assert r.status_code == 200
    cycles = r.get_json()['cycles']
    assert len(cycles) > 0
    print(f"[OK] DFS Cycle Detection OK: Found {len(cycles)} cycle(s): {cycles[0]['path']}")
    r = client.post('/api/detect/shortest-path', json={'source': 'ACC-901', 'target': 'ACC-999'})
    assert r.status_code == 200
    path_res = r.get_json()['result']
    assert path_res['found'] is True
    print(f"[OK] Dijkstra Shortest Path OK: {path_res['path']} (Total Hops: {path_res['hop_count']})")
    r = client.get('/api/detect/smurfing')
    assert r.status_code == 200
    patterns = r.get_json()['patterns']
    assert len(patterns) > 0
    print(f'[OK] BFS Smurfing Detection OK: Found {len(patterns)} pattern(s)')
    r = client.get('/api/search/trie?q=ACC-10')
    assert r.status_code == 200
    matches = r.get_json()['matches']
    assert len(matches) > 0
    print(f'[OK] Trie Autocomplete OK: Found {len(matches)} match(es)')
    r = client.get('/api/search/account?id=ACC-101')
    assert r.status_code == 200
    acc = r.get_json()['account']
    assert acc['account_id'] == 'ACC-101'
    print(f"[OK] Hash Table O(1) Lookup OK: Account {acc['account_id']} - {acc['name']}")
    r = client.get('/api/filter/bst?min=9000&max=10000')
    assert r.status_code == 200
    bst_res = r.get_json()
    assert bst_res['count'] > 0
    print(f"[OK] BST Range Query OK: Found {bst_res['count']} transaction(s) between $9,000 and $10,000")
    r = client.get('/api/buffer/state')
    assert r.status_code == 200
    buf_data = r.get_json()['buffer']
    assert 'slots' in buf_data and buf_data['capacity'] == 10
    print(f"[OK] Circular Queue Buffer OK: Size={buf_data['size']}/{buf_data['capacity']}")
    r = client.get('/api/matrix')
    assert r.status_code == 200
    matrix_data = r.get_json()
    print(f"[OK] Adjacency Matrix OK: {len(matrix_data['nodes'])}x{len(matrix_data['nodes'])} matrix computed")
    print('\n' + '=' * 50)
    print('ALL API ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!')
    print('=' * 50)
if __name__ == '__main__':
    test_endpoints()
