from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import aiohttp, re

app = FastAPI(
    # docs_url=None,
    # redoc_url=None
)

class Item(BaseModel):
    cmd: str
    val: int

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error":1}
    )

@app.post("/jsonplaceholder")
async def jsonplaceholder(item: Item):
    async with aiohttp.ClientSession() as session:
        async with session.get(get_restapi(item)) as response:
            return await response.json()

@app.get("/get_flag")
async def get_flag(request: Request):
    try:
        ip = request.headers['x-forwarded-for'].split(",")[-2].strip()
    except Exception as e:
        ip = request.client.host
    
    print(ip)

    if ip == '127.0.0.1':
        return "FLAG"
    return "NOT ALLOWED"

@app.get("/")
async def main():
    content = """
<body>
<form action="#" onsubmit="return view(this);">
<select id="c">
<option value="/posts">posts</option>
<option value="/todos">todos</option>
<option value="/users">users</option>
</select>
<input type="text" value="1" id="v" /><button type='submit'>read</button>
</form>
<p>https://jsonplaceholder.typicode.com/</p>
<pre id='output'>
</pre>
<script>
const view = (f) => {
    fetch('/jsonplaceholder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cmd:document.querySelector('#c').value,
            val:document.querySelector('#v').value
        })
    })
    .then(response=>response.text())
    .then(data=>document.querySelector('#output').innerHTML=data)
    return false;
}
</script>
</body>
    """
    return HTMLResponse(content=content)

def get_restapi(item):
    api = "https://jsonplaceholder.typicode.com"

    pattern = re.compile(r'^[0-9a-zA-Z./_\-?]*$')
    path = f"{item.cmd}/{item.val}"
    if not pattern.fullmatch(path):
        return f"{api}/posts/1"
    return f"{api}{path}"