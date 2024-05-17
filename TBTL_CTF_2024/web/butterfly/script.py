with open('db.txt', 'r') as f:
    content = ''.join(f.read().splitlines())
    print(content)

KEY = 'very secure'