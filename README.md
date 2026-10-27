# Bank Fraud Detection System (DSA Microproject – 03)

**Industry Focus:** Banking, Cybersecurity, Financial Services  
**Integrated Course Outcomes:** **CO1, CO2, CO3, CO4, CO5**  
**Technology Stack:** Python 3 (Custom Data Structures from scratch), Flask, HTML5, CSS3, JavaScript (Canvas & Chart.js)

---

## 1. Project Overview & Scope

Modern financial criminals use complex techniques like **circular money laundering rings**, **smurfing (structuring transactions into small chunks)**, and **money mule relay networks** to bypass traditional rule-based banking filters.

This microproject models a bank's transactional ledger as a **Directed Weighted Graph** $G = (V, E)$:
* **Vertices ($V$):** Bank Accounts / Customers (Account ID, Name, Risk Score, Balance, Sanction Flag).
* **Edges ($E$):** Directed Transactions (Source, Destination, Amount, Timestamp, Transaction ID).

By combining graph traversal techniques (**DFS, BFS, Dijkstra**) with linear, searching, sorting, and hierarchical data structures (**Circular Queue, Deque, Doubly Linked List, Hash Table, BST, Trie, Min/Max Heap**), the system identifies and visualizes financial crime in real time.

---

## 2. Comprehensive Course Outcome (CO) Mapping

Every single module strictly implements syllabus concepts from **Learning Units I through V**:

| Course Outcome | Learning Unit | Syllabus Topic & Implementation in Fraud Detection System | Theoretical Time Complexity |
| :--- | :--- | :--- | :--- |
| **CO1: Stacks & Queues** | **Unit I** | • **Circular Queue:** Real-time streaming transaction buffer with wrap-around `% capacity` and Front/Rear pointers.<br>• **Deque (Double-Ended Queue):** Sliding-window transaction velocity monitor to detect high-frequency burst attacks.<br>• **Priority Queue (Heap):** High-severity fraud alert scheduling (Critical $\to$ High $\to$ Medium).<br>• **Stack ADT:** Backtracking & cycle path reconstruction during DFS. | Enqueue/Dequeue: $O(1)$<br>Deque push/pop: $O(1)$<br>Priority Queue push/pop: $O(\log N)$ |
| **CO2: Linked Lists & Search** | **Unit II** | • **Singly Linked List:** Core representation of graph adjacency lists & hash table chaining buckets.<br>• **Doubly Linked List:** Transaction audit ledger enabling forward & backward audit inspection.<br>• **Sequential vs. Binary Search:** Performance comparison on transaction log queries. | Linked List Insert: $O(1)$<br>Sequential Search: $O(N)$<br>Binary Search: $O(\log N)$ |
| **CO3: Searching & Sorting** | **Unit III** | • **Hash Table with Chaining:** $O(1)$ average lookup for accounts and blacklisted entities.<br>• **Merge Sort:** $O(N \log N)$ stable sorting for transaction logs by amount/timestamp.<br>• **Bubble, Selection, Insertion Sort:** Benchmarking $O(N^2)$ quadratic algorithms against Merge Sort.<br>• **Interpolation Search:** Fast $O(\log \log N)$ probe search on uniform transaction distributions. | Hash Table: $O(1)$ avg<br>Merge Sort: $O(N \log N)$<br>Quadratic Sorts: $O(N^2)$<br>Interpolation Search: $O(\log \log N)$ |
| **CO4: Trees & Heaps** | **Unit IV** | • **Min-Heap (Array-based):** Powers Dijkstra’s shortest path algorithm ($O((V+E)\log V)$).<br>• **Max-Heap:** Extracts Top-$K$ highest-value or highest-risk transactions.<br>• **Binary Search Tree (BST):** Fast range queries $[V_{min}, V_{max}]$ for transaction amounts without full table scans.<br>• **Trie (Prefix Tree):** Instant $O(L)$ prefix autocomplete for Account Numbers & Customer Names. | Heap Insert/Extract: $O(\log N)$<br>BST Search/Insert: $O(\log N)$ avg<br>Trie Lookup: $O(L)$ where $L = \text{length}$ |
| **CO5: Graph Theory** | **Unit V** | • **Adjacency List & Matrix:** Dual graph representations demonstrating sparsity vs density tradeoffs.<br>• **DFS (Cycle Detection):** 3-color state machine (White/Gray/Black) to uncover circular money laundering rings ($A \to B \to C \to A$).<br>• **BFS Traversal:** Multi-hop fund dispersal ($k$-hop layering) and fan-out/fan-in smurfing.<br>• **Dijkstra's Algorithm:** Traces shortest suspicious mule chains from sanctioned sources to cash-out points. | DFS / BFS: $O(V + E)$<br>Dijkstra: $O((V + E) \log V)$<br>Matrix Gen: $O(V^2)$ |

---

## 3. Project Directory Structure

```
DSA_Project/
├── app.py                             # Flask Web Server & REST API endpoints
├── README.md                          # Project Documentation and Course Outcome Mapping
├── data/
│   └── transactions_dataset.json      # Realistic synthetic dataset (Normal + 4 Fraud Scenarios)
├── dsa/
│   ├── linear/                        # [CO1 & CO2]
│   │   ├── linked_list.py             # Singly, Doubly, and Circular Linked Lists
│   │   ├── stack.py                   # Stack ADT (Array & Linked List based)
│   │   ├── queue.py                   # Standard Queue, Circular Queue, Priority Queue
│   │   └── deque.py                   # Double-Ended Queue for sliding windows
│   ├── searching_sorting/             # [CO2 & CO3]
│   │   ├── hash_table.py              # Hash Table with Chaining and Open Addressing
│   │   ├── sorting.py                 # Bubble, Selection, Insertion, and Merge Sort
│   │   ├── searching.py               # Sequential, Binary (Iter/Rec), Interpolation Search
│   │   └── benchmark.py               # Empirical runtime benchmarking harness
│   ├── trees/                         # [CO4]
│   │   ├── heap.py                    # Min-Heap, Max-Heap, Heap Priority Queue
│   │   ├── bst.py                     # Binary Search Tree with In/Pre/Post traversals & AVL
│   │   └── trie.py                    # Trie for prefix account search
│   └── graphs/                        # [CO5]
│       ├── graph.py                   # Directed Graph (Adjacency List & Matrix)
│       ├── dfs_cycles.py              # DFS Cycle Detection for Money Laundering
│       ├── bfs_traversal.py           # BFS for Layering and Smurfing (Fan-out/Fan-in)
│       └── dijkstra.py                # Dijkstra Shortest Path using Min-Heap
├── engine/
│   └── fraud_detector.py              # Orchestrator integrating all DSA modules
├── tests/
│   ├── test_dsa.py                    # 12 Unit tests verifying core data structures
│   └── test_api.py                    # Integration test verifying all API endpoints
└── web/
    ├── templates/
    │   └── index.html                 # Interactive Web Dashboard
    └── static/
        ├── css/
        │   └── styles.css             # Cybersecurity & Banking visual design
        └── js/
            ├── graph_visualizer.js    # Canvas-based interactive directed graph engine
            └── app.js                 # API bridge, live alerts, and Chart.js benchmarks
```

---

## 4. Setup and Execution Instructions

### Prerequisites
* Python 3.10+ installed
* Flask (Installed via `pip install flask`)

### Running the Web Application
```bash
python app.py
```
Then open your web browser at:
```
http://127.0.0.1:5000
```

### Running the Automated Unit Test Suite
To verify all custom data structures from CO1 to CO5:
```bash
python -m unittest tests/test_dsa.py
```

### Running the API Integration Test
To verify all REST API endpoints:
```bash
python tests/test_api.py
```

---

## 5. Walkthrough of Interactive Web Features

1. **Interactive Canvas Graph Visualization:**
   * Nodes represent bank accounts color-coded by risk level (Green = Safe, Amber = Intermediary, Red = Flagged/High Risk).
   * Pan, zoom, and drag nodes freely with the mouse.
   * Directed arrows display real-time transaction amounts.
2. **DFS Cycle Detection (Money Laundering Rings):**
   * Click **"Scan for Circular Laundering Rings (DFS)"**.
   * Identifies closed cycles such as `ACC-101 ➔ ACC-102 ➔ ACC-103 ➔ ACC-104 ➔ ACC-101` and animates them in **glowing neon red** on the canvas.
3. **Dijkstra Shortest Path (Suspicious Mule Chain):**
   * Select a sanctioned source (e.g., `ACC-901`) and a cash-out terminal (e.g., `ACC-999`).
   * The custom **Min-Heap** calculates the minimum-hop path, highlighting the mule relay chain in **neon cyan**.
4. **BFS Smurfing & Layering:**
   * Click **"Scan for Smurfing & Layering (BFS)"** to identify structuring patterns (e.g. `ACC-200` dispersing funds across 5 distinct mule accounts).
   * Level-order BFS displays fund dispersal reachability trees.
5. **Trie Autocomplete & Hash Table Lookup:**
   * In the Search tab, type `ACC-1` or `Smurf` into the input. The **Trie** instantly auto-completes matches.
   * Clicking a result fetches complete profile details from the **Hash Table** in $O(1)$ time.
6. **BST Range Search:**
   * Enter min/max transfer amounts to query the **Binary Search Tree** and inspect in-order sorted traversal tags.
7. **Circular Queue Ingestion Buffer:**
   * View live slots of the fixed-capacity **Circular Queue** with active **Front (F)** and **Rear (R)** pointers.
   * Submit live transactions through the form and observe dynamic queue wrap-around and sliding-window velocity checks via **Deque**.
8. **Empirical Benchmarks (CO3):**
   * Interactive charts dynamically compare execution times of **Merge Sort** vs. $O(N^2)$ sorts and **Interpolation Search** vs. **Binary Search**.
