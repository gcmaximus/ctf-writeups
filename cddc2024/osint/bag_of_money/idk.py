hi = 'bafybeicjfojuswk3uzb54f76qxmwcfkf7tpf3lxg6u36mazkjk5a2gtybq'

print()
for char in hi:
    if char.isnumeric():
        print(char, end='')

print()
for char in hi:
    if not char.isnumeric():
        print(char, end='')