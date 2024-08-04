# crypto/not-quite-caesar
Caesar??? Couldn't be this!

# Flag
```
vsctf{looks_like_ceasar_but_isnt_a655563a0a62ef74}
```

# Solution
Random initialised internal state is always set with seed `1337`, hence `random.choice` will always pick the same lambda functions in the same order at every runtime of the code. 

Reverse the order of operations for each lambda.

See `solve.py`.