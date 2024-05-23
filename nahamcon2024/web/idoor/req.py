import hashlib
import requests

base = 'http://challenge.nahamcon.com:31646/'

for i in range(20):
    digest = hashlib.sha256(str(i).encode('utf-8')).hexdigest()
    print(f'{i}: {digest}')
    x = requests.get(base + digest)
    if 'Not Found' in x.text:
        pass
    else: 
        print(x.text)
        break
