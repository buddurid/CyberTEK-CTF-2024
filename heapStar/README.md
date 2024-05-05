a fairly easy heap challenge , the challenge basically provides a source code and a win condition . You cant ask for more .  
lets start by checksec'ing the binary . 

![img](/imgs/1-checksec.png)

no pie , that's gonna help . 

now lets break down what the binary does 
1. allocate a chunk of whatever size you want , and read to it with a possibly infinite overflow due to the vulnerable function **getInput(ptr)**

```
void getInput(char *buffer) {
  int i = 0;
  char c;
  printf("Data: ");
  while ((c = getchar()) != '\n' && c != EOF) {
    buffer[i++] = c;
  }
  buffer[i] = '\0';
}
```
getIndex keeps receiving input until it receives "\n" char.

2. free a chunk , then sets its pointer in the array to 0 . we can create a **use after free** with the overflow we have so no biggie . 

3. edit a chunk with the same function **getInput(ptr)** so that means trouble . 

4. we can get a shell if the **target** variable which is set initially to null somehow gets changed .  

#### the plan 

* **target** is a global variable , and we know that pie is disabled >>> we know the address of **target**
* no leak possiblity 
* we have a use after free vuln 
* we dont have to actually get code execution as there is win condition provided by the binary

>>> in my case , i used a large bin attack to put a heap value in the **target** . if you dont know this technique , i recommend this PoC by [h0w2heap](https://github.com/shellphish/how2heap/blob/master/glibc_2.35/large_bin_attack.c) in addition to lots of other houses . 

to sum up how this works : 
1. allocate a big chunk (that fits into large bin) + another chunk to prevent consolidation
2. allocate a big chunk (a bit smaller than the first chunk but that fits in the same large bin) + another chunk to prevent consolidation
3. free chunk 1 then allocate a chunk bigger than its size to put it into the large bin
4. free chunk 2 to put it into unsorted bin
5. put **&target-0x10** into the bkd_nextsize field of chunk 1 , doesnt matter if you overwrite the first fields with junk
6. allocate a chunk bigger than both chunks to put chunk 2 into the large bin 
7. during the insertion of chunks 2 into large bin , its address is gonna be written into **&target-0x10+0x10**

just like that we get our first flag . check out my solver if you wanna . 

[flag](/imgs/1-flag.png)
