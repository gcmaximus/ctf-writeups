# rev/intro-reversing
Flag will be printed out straight away when you run the binary.

# Flag
```
vsctf{1nTr0_r3v3R51ng!}
```

# Solution
Patch the binary to change the sleep function to `sleep(0)` so that flag is instantly printed out.