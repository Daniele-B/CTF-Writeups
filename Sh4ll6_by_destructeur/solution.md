# Solution

I've menaged to solve this crackme using only black box tricks and some guessing


This crackme is clearly [UPX](https://upx.github.io) packed, we can find the ```This file is packed with the UPX executable packer http://upx.sf.net``` string in it.
So let's unpack it! 
```
>./upx -d -o Sh4ll6_unpacked Sh4ll6

                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2017
UPX 3.94        Markus Oberhumer, Laszlo Molnar & John Reiser   May 12th 2017

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
  10324076 <-   2624040   25.42%   linux/i386    Sh4ll6_unpacked

Unpacked 1 file.

```

Now, let's move on with another black box trick used when you reverse on Linux: ltrace

```
>ltrace ./Sh4ll6_unpacked

sigaction(SIGSEGV, { 0x8048280, <>, 0, nil }, nil)                                                                                = 0
sigaction(SIGILL, { 0x8048307, <>, 0, nil }, nil)                                                                                 = 0
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGILL (Illegal instruction) ---
--- SIGSEGV (Segmentation fault) ---
fgets(òlfmeoer
"\303\262lfmeoer\n", 13, 0xf7ef6720)                                                                                        = 0x860f188
--- SIGSEGV (Segmentation fault) ---
printf("%c", 'B')                                                                                                                 = 1
.
.
.
--- SIGILL (Illegal instruction) ---
--- SIGSEGV (Segmentation fault) ---
printf("%c", 'r')                                                                                                                 = 1
--- SIGILL (Illegal instruction) ---
--- SIGSEGV (Segmentation fault) ---
exit(1Bad password, looser <no return ...>
+++ exited (status 1) +++
```

What we notice here is that the password must be maximum 13 charcher long.<br/>
Another thing we can see is that the binary uses sigaction to handle SIGSEGV and SIGILL signals, then it triggers them.
Sometimes these kind of stuff are used as antidebugger tricks.

If you open a disassembler now what you will see is only mov instructions, and if you are enougth in the business of reversing you will catch immediatly what it means: the binary is obfuscated with [Movfuscator](https://github.com/xoreaxeaxeax/movfuscator.git).
<br/>[asm86 Mov instruction is turing complete](https://www.cl.cam.ac.uk/~sd601/papers/mov.pdf), which basically means you can replace any other asm86 instruction with a bunch of mov. Cool! Isn't it? Movfuscator does exactly this (and adds some antidebug tricks, alredy described).

So now how do we retrive the original instructions?<br/>
Have original instrutions back is a painful job but there is an experimental deobfuscator, and we can use it.<br/>
[Demovfuscator](https://github.com/kirschju/demovfuscator.git) doesn't retrive the instructions but its very helpful because it removes the annoyng sigaction stuff and, most important, it can give us the original program control flow.
This is the control flow of our crackme:<br/>
![alt text](https://raw.githubusercontent.com/Daniele-B/Crackmes-Solutions/master/Sh4ll6_by_destructeur/cfg.png)

the binary has 13 "false blocks" on the right side of the graph, my guess is it checks char by char the flag and it follows these blocks if the selected char is right.
Then it performs a print. The "good boy" string is printed at block 0x8060e03, the "bad boy" at 0x8062faf<br/>
When a binary performs a char by char check it makes me happy because i can use [Valtool](https://github.com/Daniele-B/Valtool.git) to bruteforce the flag and win without too much effort.
Let's try:<br/>
```>python Valtool.py -l 13 -c 6 -s _ Sh4ll6_cf_restored```

Outupt is pretty ugly beacuse it cannot handle segfault well, but it worked!
Our flag is ```0bfuscated=!```

```
>./Sh4ll6
0bfuscated=!
Good password! GG!!!
```

It seems last 2 chars are ignored so we'll ignore them too. :P
