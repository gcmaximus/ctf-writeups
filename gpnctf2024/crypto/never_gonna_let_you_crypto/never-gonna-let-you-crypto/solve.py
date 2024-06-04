

with open('FLAG.enc', 'r') as f:
    enc = bytearray.fromhex(f.read())

enc_start = enc[:5]
print(enc)

key = []
plain = b'GPNCT'

for i in range(len(enc_start)):
    # print(enc_start[i])
    # print(plain[i])
    # print(enc_start[i] ^ plain[i])
    key.append(enc_start[i] ^ plain[i])

print(key)

for i in range(len(enc)):
    print(chr(enc[i] ^ key[i%5]), end='')

print()