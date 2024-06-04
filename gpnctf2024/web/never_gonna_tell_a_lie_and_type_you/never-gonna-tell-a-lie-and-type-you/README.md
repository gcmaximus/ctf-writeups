# Never gonna tell a lie and type you
todo

# Flag
```
GPNCTF{1_4M_50_C0NFU53D_R1GHT_N0W}
```

# Solution
We need to bypass some basic checks such as modifying User-Agent and sending POST data.

From the PHP file, we can see that this function is used to check if the user can run OS commands:

```php
function securePassword($user_secret){
    if ($user_secret < 10000){
        die("nope don't cheat");
    }
    $o = (integer) (substr(hexdec(md5(strval($user_secret))),0,7)*123981337);
    return $user_secret * $o ;
    
}
```

However, the type is not checked as seen in the use of `==` instead of `===`:

```php
if ($user_input->{'password'} == securePassword($user_input->{'password'})  ){
            echo " hail admin what can I get you ". system($user_input->{"command"});
        }
```

So, as long as `securePassword($user_input->{'password'})` returns a non-zero number, by inputing the boolean `True`, the condition will always render True and we can send a command to read the flag file.

See `req.py` for script.