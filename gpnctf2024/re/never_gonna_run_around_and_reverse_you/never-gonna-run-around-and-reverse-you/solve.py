import subprocess

with open('hash', 'r') as f:
    flag = f.read()

plain = ""

for j in range(0,len(flag), 2):

    test = flag[0:j+2]

    for i in range(33,127):
        char = chr(i)
        user_input = plain + char
        cmd = ['./hasher', user_input]
        result = subprocess.run(cmd, capture_output=True,text=True).stdout.strip()

        if result == test:
            print('Plaintext:',  user_input)
            plain += char
            break


print('Flag :) >>',plain)