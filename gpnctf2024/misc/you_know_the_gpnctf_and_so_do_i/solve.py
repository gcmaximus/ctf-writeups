with open('lyrics.txt', 'r') as f:
    content = f.read()

print(content.replace('\n', ''))