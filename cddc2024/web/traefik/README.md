# Traefik
Welcome to Traefik
https://traefik.cddc2024.com

Flag format : CDDC24{   }

# Flag
CDDC24{I_WANT_TO_J0NA1_D3VIC3S}

# Solution
In `docker-compose.yml` given, there are some credentials present at the end of the file:

```
- "traefik.http.middlewares.auth.basicauth.users=traefik:$$apr1$$vLnO2ns1$$mNpO3B5WQ5/sDBSfpjT6D/"
```

Use hashcat to crack the password (Apache htpasswd format, method 1600)

Login and browse to `/flag.txt`