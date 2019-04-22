import RPi.GPIO as GPIO
from time import sleep
import lirc

led=24
def ledBlinking():
	for x in range(0,10):
		GPIO.output(led,True)
		sleep(0.05)
		GPIO.output(led,False)
		sleep(0.05)
def gpioChState(x):
	if GPIO.input(x) == 0:
		GPIO.output(x,True)
	else:
		GPIO.output(x,False)

#################################################################################
#										#
#	na poczatek instalacja lirc i pylirc i konfiguracja pilota w lirc	#
#       rbpl.blogspot.com/2013/01/odbiornik-podczerwieni.html			#
#	WPROWADZIC WSZYSTKIE KLAWISZE DO PLIKU pylircrc w katalogu glownym	#
#	plik lircrc.conf w /etc/lirc musi byc tez zaprogramowany i znac pilot	#
#	jak zrobic zeby pilot nie pisal w terminalu?				#
#	Kodowanie pilota: Silvercrest - AUX2 (6000)				#
#										#
#################################################################################

sockid=lirc.init("myprogram", "./pylircrc")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
while 1:
	code = lirc.nextcode()
	if len(code) > 0:
		c=code[0]
		if c == "1":	
			gpioChState(led)
		elif c == "2":
			GPIO.output(led,True)
		elif c == "3":
			GPIO.output(led,False)
		else:
			print("Unsopported key (in code)")
			ledBlinking()
	else:
		print("Unsopported key (in lib)")	
		ledBlinking()
	sleep(0.05)

