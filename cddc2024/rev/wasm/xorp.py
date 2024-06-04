def str_to_bytes(string):
    bytes_hex = ' '.join(hex(char) for char in string.encode('utf-8'))
    bytes_dec = ' '.join(str(int(byte, 16)) for byte in bytes_hex.split())
    return bytes_dec

def bytes_to_str2(byte_string):
    byte_list = byte_string.split()
    hex_list = [hex(int(byte))[2:] for byte in byte_list]  # Convert bytes to hexadecimal strings
    byte_array = bytearray.fromhex(''.join(hex_list))  # Convert hexadecimal strings to bytes
    decoded_string = byte_array.decode('utf-8')  # Decode bytes to string using UTF-8 encoding
    return decoded_string

# inverse the encoding
def bytes_to_str(hex_str):
    bytes_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
    return bytes_list

# Undo changes apparently = last encoding
def undo_changes(memArr):
    result = []
    print('HI')
    # for byte in memArr:
    #     print(byte)
    #     print(hex(byte)[2:])
    #     print("00" + hex(byte)[2:])
    #     result += ("00" + hex(byte)[2:])[-2:]

    for i in range(0,len(memArr),2):
        byte = "0x" + memArr[i:i+2]
        # hex_byte = hex(byte)
        # print(hex_byte)
        integer = int(byte, 16)
        # hex_value = hex(integer)

        result.append(integer)




    return result

def encode(a, arr):
    b = 0
    while b < a - 1:
        c = b
        while c < a - 1:
            d = arr[c]
            e = arr[c+1]
            e = d ^ e
            arr[c+1] = e
            c += 1
        b += 1
    return arr

test = 'THIS_IS_A_FAKE_FLAG'
test = str_to_bytes(test)

array = test.split(' ')
print(type(array[0]))
i = 0
while i < len(array):
    array[i] = int(array[i])
    i += 1
print(type(array[0]))

length = len(array)

print(array, length)

# potential b/c < a - 1/+1

answer = encode(length, array)
        
print(answer, 'answer')

# # 541c49061616531c040815190d0e5f121a0b0d
# def decode(a, arr):
#     b = a -1
#     while b >= 1:
#         c = b - i
#         while c != b:
#             d = arr[c]
#             e = arr[c-1]
#             e = d ^ e
#             arr[c] = e
#             c += 1
#         b -= 1
#     return arr








answer_pls = "571653080c6e350c6b0f01196d06436075756365"
decoded = undo_changes(answer_pls)
print('AAAAAAAAAA', decoded)
#decoded = decoded[::-1]
# print(decoded)
# plaintext = decode(len(decoded), decoded)
#plaintext = [bytes_to_str2(num) for num in plaintext]



# # Example usage:
# hex_str = "541c49061616531c040815190d0e5f121a0b0d"  # Example hexadecimal string
# original_str = bytes_to_str(hex_str)
# print(original_str, 'inversed of encoding')

# # python converted encoding

# result = undo_changes(answer)
# print(result, 'Final result')

#"571653080c6e350c6b0f01196d06436075756365"

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


result = decode(len(decoded), decoded)

for char in result:
    print(chr(char),end='')

