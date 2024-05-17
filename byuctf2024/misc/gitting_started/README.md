# Gitting Started
A local hacker, TheITFirefly, who started up a blog to talk about his exploits in the tech world, has hidden a flag in the source code for his blog. Luckily, his source code is publicly available in a git repo!

https://gitlab.com/TheITFirefly/tech-blog

# Flag
byuctf{g1t_gud!}

# Solution
Check the commit history. Under the commit titled `Fix accidental tracking of dynamically created resources`, the following line was added in `content/posts/my-first-post.md`:

```
Fun fact, git has some weirdness in how it stores commits. byuctf{g1t_gud!}
```