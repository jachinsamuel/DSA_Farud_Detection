def sequential_search(arr, target, key=lambda x: x):
    comparisons = 0
    for idx, item in enumerate(arr):
        comparisons += 1
        if key(item) == target:
            return (idx, comparisons)
    return (-1, comparisons)

def binary_search_iterative(arr, target, key=lambda x: x):
    low = 0
    high = len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_val = key(arr[mid])
        if mid_val == target:
            return (mid, comparisons)
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    return (-1, comparisons)

def binary_search_recursive(arr, target, key=lambda x: x):
    comparisons = [0]

    def _rec(low, high):
        if low > high:
            return -1
        comparisons[0] += 1
        mid = (low + high) // 2
        mid_val = key(arr[mid])
        if mid_val == target:
            return mid
        elif mid_val < target:
            return _rec(mid + 1, high)
        else:
            return _rec(low, mid - 1)
    idx = _rec(0, len(arr) - 1)
    return (idx, comparisons[0])

def interpolation_search(arr, target, key=lambda x: x):
    low = 0
    high = len(arr) - 1
    comparisons = 0
    while low <= high and target >= key(arr[low]) and (target <= key(arr[high])):
        comparisons += 1
        if key(arr[low]) == key(arr[high]):
            if key(arr[low]) == target:
                return (low, comparisons)
            return (-1, comparisons)
        val_low = key(arr[low])
        val_high = key(arr[high])
        pos = low + int((target - val_low) * (high - low) / (val_high - val_low))
        if pos < low or pos > high:
            break
        pos_val = key(arr[pos])
        if pos_val == target:
            return (pos, comparisons)
        elif pos_val < target:
            low = pos + 1
        else:
            high = pos - 1
    return (-1, comparisons)
