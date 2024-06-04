import ascii
import sys
import string
import os
import subprocess

ascii_chars = []
for i in range(32, 127):
    if chr(i) != 33 and chr(i) != 39:
        ascii_chars.append(chr(i))

answer = "🤢😥😇😴🐭🦊😥✊✌️🍕🐰😴🍎🐭👌🐰🤢😴"


valid = []
for answer_index in range(len(answer)):
    print(answer_index)
    if answer_index == 0:
        guess = [""]
    else:
        guess = valid
        valid = []
    for char in guess:
        i = 0
        while i < len(ascii_chars):
            new_guess = char + ascii_chars[i]
            # print("XX", char)
            cmd = ["./emoji32", new_guess]
        
            execute_guess = subprocess.run(cmd, capture_output=True, text=True).stdout
            if execute_guess == answer:
                print('ANSWER FOUND: ', new_guess)
                break
            if execute_guess[:answer_index+1] == answer[:answer_index+1]:
                valid.append(new_guess)

            i += 1
# 5 = 1min
# 6 = 6 min 55