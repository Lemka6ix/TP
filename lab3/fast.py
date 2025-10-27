m = list(map(int, input().split()))
s = input().split()


def fast_sort(arr):
    if len(arr) < 1:
        return arr
    
    stack = [(0, len(arr) -1)]
    while stack:
        low, high = stack.pop()

        if low < high:
            cent = part_iter(arr, low, high)
            stack.append((low, cent - 1))
            stack.append((cent+1, high))
    return arr


def part_iter(arr, low, high):
    mid = (low + high) // 2
    centr = arr[mid]

    arr[mid], arr[high] = arr[high], arr[mid]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= centr:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
 

print('\n___result___')
fast_sort(m)
fast_sort(s)

print(*m)
print(*s)