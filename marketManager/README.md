a lil bit harder heap challenge than the first one , still doable . 

checksec:

![checksec](/imgs/2-checksec.png)

the main functionnalities of the program : 
1. malloc chunk of size <=0x80
2. delete chunk without nulling its pointer >>> use after free
3. edit chunk but within the boundaries of the allocation
4. print content of chunk even when its free as its pointer isnt nulled out .

###### notes about libc version : 
in the most recent libc versions , a new feature was introduced which is **safe Linking** for tcache -[ressources](https://www.researchinnovations.com/post/bypassing-the-upcoming-safe-linking-mitigation)- . but it is still bypassable if we leak any mangled pointer . plus we can leak libc if we fill in tcache with 7 chunks , the next freed chunk of the same size (if not in fast-bin) will have libc pointer so we leak it . 

ok now we have heap and libc leak and arbitrary write as we can corrupt tcache next pointers . 
###### Then what ? What do we overwrite ?

overwriting the heap wont give us code execution . so our target is **libc** . there might be some other ways to do it , but i prefer to overwrite the stdout struct in libc in what is known **file struct exploit** . Wont go in depth on what happens , but you need to manipulate the ```Vtable and the wide_data``` of the struct in a way that will cause system to be called, and inject a string that is gonna get executed by system in the **flags field** of the struct , in my case i used ```system("Junk;sh")```

check this [link](https://dhavalkapil.com/blogs/FILE-Structure-Exploitation/) for further reading and understanding . 

![flag](/imgs/2-flag.png)

