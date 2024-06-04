# Never gonna give you UB
Can you get this program to do what you want?

# Flag
```
GPNCTF{G00d_n3w5!_1t_l00ks_l1ke_y0u_r3p41r3d_y0ur_disk...}
```

# Solution
This is a simple 64-bit buffer overflow to control the return address.

```c
void scratched_record() {
	printf("Oh no, your record seems scratched :(\n");
	printf("Here's a shell, maybe you can fix it:\n");
	execve("/bin/sh", NULL, NULL);
}
```

The vulnerability lies in the `gets()` function used. The buffer is 255 bytes.

```c
int main() {
	printf("Song rater v0.1\n-------------------\n\n");
	char buf[0xff]; //255 bytes
	printf("Please enter your song:\n");
	gets(buf); // OVERFLOW <<
	printf("\"%s\" is an excellent choice!\n", buf);
	return 0;
}
```

Running through the basic `cyclic 300` and running in gdb tells us that out payload needs to consist of 264 bytes of padding, followed by the 8-byte return address (in little endian). After we get the shell, `cat /flag` to get the flag.

See `solve.py`.