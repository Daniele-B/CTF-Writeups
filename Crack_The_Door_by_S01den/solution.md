#solution
This is a really easy crackme based on xor "encryption", the first i did on crackmes.one

original crackme link: https://crackmes.one/crackme/5b5b386033c5d46b771434b8

All the stuff we need are in the main function.<br/>
This function starts with printing some fancy text/ascii art to explain what we have to do, but we can ignore them during reversing.<br/>
Then it asks for a username througth an fgets, the username we write goes into a local variable positioned at rbp-0x80. We already know what the username is: "Razpakhomon".<br/>
Then it asks for a password, the length must be 12 otherwise the binary jumps to "BAD LENGTH". Password is stored immediatly after the username at rpb-0x70.<br/>
The check part is just a for loop starting at 0x40160c which basically do this:

```c
for (int j = 0; j <= 10; j += 2 )
 {
    arr[j] = ((first_string[j] + 50) ^ username[j]) % 100 + 65;
    arr[j + 1] = second_string[(9 * j + 5) % 12];
    if ( count == j && arr[j] == password[j] && arr[j + 1] == password[j + 1] )
      count += 2;
 }
if (count == 12)
	puts("OK");
else
	puts("NOPE");
```

where: first_string = ```THEPIRATEISZ```, second_string = ```?*-/597$=#&@```, count = 0<br/>
the first_string and second_string are just 2 string in the stack, count is an int32 local variable.<br/>
The for loop iterates 6 times, so in order to get count == 12 we have to supply the first if condition at every iteration.<br/>
To do that we can do a trick for lazy people like me: debug the binary, put a breakpoint after the for loop and dump arr.<br/>
And there we go our solution: ```M9N@[9\@[9d@```
