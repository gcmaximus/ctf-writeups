def decode(a, arr):
    for i in range(2, a+1):
        k = 1
        while k < i:
            # operations
            d = arr[-1*k]
            e = arr[-1*k-1]
            d = d ^ e
            arr[-1*k] = d
            k += 1
    return arr
print(decode(3, [54, 119, 73]))
result = decode(20,[87, 22, 69, 77, 65, 57, 95, 91, 60, 93, 105, 124, 122, 115, 49, 72, 80, 53, 70, 75])
a = [87, 22, 83, 8, 12, 110, 53, 12, 107, 15, 1, 25, 109, 6, 67, 96, 117, 117, 99, 101]
result = decode(len(a), a)

for char in result:
    print(chr(char),end='')

