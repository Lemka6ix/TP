m = list(map(int, input().split()))

def vstav(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

vstav(m)
print(*m)


s = input().split()

vstav(s)
print(*s)

