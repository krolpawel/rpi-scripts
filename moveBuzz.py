import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(21,GPIO.IN)

while 1:
	if GPIO.input(21) == 1:
		GPIO.output(24,True);
	else:
		GPIO.output(24,False);


