import lirc
from time import sleep
print("Codes:")
sockid=lirc.init("myprogram", "./pylircrc")
while 1:
	code = lirc.nextcode()
	if code[0] == "1":	
		print("w iofie")
	print("C: "+code[0])
	sleep(1)

