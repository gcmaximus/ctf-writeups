# Random
I've only had the time to make the API, but it should be working properly. Please make sure it's secure. If you can read any file you want, I'll make sure to reward you!

# Flag
byuctf{expl01t_chains_involve_multiple_exploits_in_a_row}

# Solution
1. Find the APP_SECRET using current time. Run `getsecret.py` to get JWT token to be authenticated

2. Pass in `/etc/passwd` as filename argument in the GET /api/file API. This will show the home directory (which is a random string) for the user, where the flag is stored. 

```
ctf:x:1000:1000::/439f4860b2c8e9cc50bf2e5dca2e442f:/bin/sh
```

3. View flag file through `https://random.chal.cyberjousting.com/api/file?filename=/439f4860b2c8e9cc50bf2e5dca2e442f/flag.txt`