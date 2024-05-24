import base64

with open('theflag', 'rb') as f:
    flag = f.readline()

for i in range(100):
    print('Iteration:', i+1)


    flag = base64.b64decode(flag)
    if len(flag) < 100:
        print(flag)
    
    if b'flag' in flag:
        break
