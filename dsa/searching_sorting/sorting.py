def bubble_sort(arr, key=lambda x: x):
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if key(a[j]) > key(a[j + 1]):
                a[j], a[j + 1] = (a[j + 1], a[j])
                swaps += 1
                swapped = True
        if not swapped:
            break
    return (a, comparisons, swaps)

def selection_sort(arr, key=lambda x: x):
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if key(a[j]) < key(a[min_idx]):
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = (a[min_idx], a[i])
            swaps += 1
    return (a, comparisons, swaps)

def insertion_sort(arr, key=lambda x: x):
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0
    for i in range(1, n):
        current_val = a[i]
        current_key = key(current_val)
        j = i - 1
        while j >= 0:
            comparisons += 1
            if key(a[j]) > current_key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = current_val
    return (a, comparisons, shifts)

def merge_sort(arr, key=lambda x: x):
    comparisons = [0]

    def _merge_sort(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr
        mid = len(sub_arr) // 2
        left = _merge_sort(sub_arr[:mid])
        right = _merge_sort(sub_arr[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    sorted_result = _merge_sort(list(arr))
    return (sorted_result, comparisons[0])
