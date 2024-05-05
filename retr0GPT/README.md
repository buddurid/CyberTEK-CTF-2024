this one is a good and straightforward ROP challenge .

![img](/imgs/3-checksec.png)


the binary we are provided asks for input in an infinite loop until our input starts with **"e"** .we can overflow the stack since there are no restrictions on the size . so our normal plan would be to puts(puts) into restart into ret2libc , well that requires both puts and pop_rdi gadget . Guess what ? we dont have both xD . 

* we can replace **puts** with **printf**
* we can make use of the gift the binary offers . 

![gift](/imgs/3-gift.png)

looks like we are given an opportunity to put whatever we want in rdi , through dereferencing [rbp-0x10] . there could be many ways to perform the leak and restart , my method was jumping to ```gift+1``` so that our desired rdi value would be **0x10** bytes away from the start of our input (in other words the saved rbp is the gonna become the rdi). look up the first payload in my solver if you get confused . 

once we perform the leak and restart , we use gadgets from libc to perform ```system("/bin/sh")``` and its GG . 

![flag](/imgs/3-flag.png)





