import random
import ast

with open('dist/out.txt','r') as f:
    data = ast.literal_eval(f.read())

print(data)
random.seed(1337)

ops = [
    lambda x: x-3,
    lambda x: x+3,
    lambda x: x/3,
    lambda x: x^3,
]

out = []

for d in data:
    out.append(chr(int(random.choice(ops)(d))))

flag = ''.join(out)

with open('flag.txt', 'w') as f:
    f.write(flag)