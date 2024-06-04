def encode(arr):
    a = len(arr)
    b = 0
    while b < a - 1:
        c = 0
        while c < a - 1:
            d = arr[c]
            e = arr[c + 1]
            e = d ^ e
            arr[c + 1] = e
            c += 1
        b += 1

# Example usage
flag_arr = [ord(char) for char in 'THIS_IS_A_FAKE_FLAG']
encode(flag_arr)

print(flag_arr)
# print(encoded_hex)
