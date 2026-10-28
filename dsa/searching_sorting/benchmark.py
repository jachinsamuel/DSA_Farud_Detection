import time
import random
from dsa.searching_sorting.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort
from dsa.searching_sorting.searching import sequential_search, binary_search_iterative, binary_search_recursive, interpolation_search

def benchmark_sorting(sizes=(50, 100, 250, 500, 1000)):
    results = {'sizes': list(sizes), 'bubble_sort': {'times_ms': [], 'comparisons': []}, 'selection_sort': {'times_ms': [], 'comparisons': []}, 'insertion_sort': {'times_ms': [], 'comparisons': []}, 'merge_sort': {'times_ms': [], 'comparisons': []}}
    for n in sizes:
        sample = [round(random.uniform(10.0, 50000.0), 2) for _ in range(n)]
        t0 = time.perf_counter()
        _, b_comp, _ = bubble_sort(sample)
        results['bubble_sort']['times_ms'].append(round((time.perf_counter() - t0) * 1000, 3))
        results['bubble_sort']['comparisons'].append(b_comp)
        t0 = time.perf_counter()
        _, s_comp, _ = selection_sort(sample)
        results['selection_sort']['times_ms'].append(round((time.perf_counter() - t0) * 1000, 3))
        results['selection_sort']['comparisons'].append(s_comp)
        t0 = time.perf_counter()
        _, i_comp, _ = insertion_sort(sample)
        results['insertion_sort']['times_ms'].append(round((time.perf_counter() - t0) * 1000, 3))
        results['insertion_sort']['comparisons'].append(i_comp)
        t0 = time.perf_counter()
        _, m_comp = merge_sort(sample)
        results['merge_sort']['times_ms'].append(round((time.perf_counter() - t0) * 1000, 3))
        results['merge_sort']['comparisons'].append(m_comp)
    return results

def benchmark_searching(sizes=(100, 500, 1000, 5000, 10000)):
    results = {'sizes': list(sizes), 'sequential': {'avg_time_ms': [], 'avg_comparisons': []}, 'binary_iterative': {'avg_time_ms': [], 'avg_comparisons': []}, 'binary_recursive': {'avg_time_ms': [], 'avg_comparisons': []}, 'interpolation': {'avg_time_ms': [], 'avg_comparisons': []}}
    TRIALS = 30
    for n in sizes:
        data = sorted(random.sample(range(1, n * 10), n))
        test_targets = random.sample(data, min(TRIALS, n))
        t0 = time.perf_counter()
        total_comp_seq = sum((sequential_search(data, t)[1] for t in test_targets))
        dur_seq = (time.perf_counter() - t0) * 1000 / len(test_targets)
        results['sequential']['avg_time_ms'].append(round(dur_seq, 4))
        results['sequential']['avg_comparisons'].append(round(total_comp_seq / len(test_targets), 1))
        t0 = time.perf_counter()
        total_comp_bin_it = sum((binary_search_iterative(data, t)[1] for t in test_targets))
        dur_bin_it = (time.perf_counter() - t0) * 1000 / len(test_targets)
        results['binary_iterative']['avg_time_ms'].append(round(dur_bin_it, 4))
        results['binary_iterative']['avg_comparisons'].append(round(total_comp_bin_it / len(test_targets), 1))
        t0 = time.perf_counter()
        total_comp_bin_rec = sum((binary_search_recursive(data, t)[1] for t in test_targets))
        dur_bin_rec = (time.perf_counter() - t0) * 1000 / len(test_targets)
        results['binary_recursive']['avg_time_ms'].append(round(dur_bin_rec, 4))
        results['binary_recursive']['avg_comparisons'].append(round(total_comp_bin_rec / len(test_targets), 1))
        t0 = time.perf_counter()
        total_comp_interp = sum((interpolation_search(data, t)[1] for t in test_targets))
        dur_interp = (time.perf_counter() - t0) * 1000 / len(test_targets)
        results['interpolation']['avg_time_ms'].append(round(dur_interp, 4))
        results['interpolation']['avg_comparisons'].append(round(total_comp_interp / len(test_targets), 1))
    return results
