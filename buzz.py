import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)

for x in range(0,3):
	GPIO.output(24,True)
	sleep(0.1)
	GPIO.output(24,False)
	sleep(0.1)

