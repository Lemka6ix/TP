m = list(map(int, input().split()))
s = input().split()


def vstav(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

print('\n___result___')

vstav(m)
vstav(s)

print(*m)
print(*s)