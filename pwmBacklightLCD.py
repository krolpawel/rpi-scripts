import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.OUT)

p=GPIO.PWM(16,50)

p.start(0)

try:
	while True:
		for i in range(100):
			p.ChangeDutyCycle(i)
			time.sleep(0.02)
		for i in range(100):
			p.ChangeDutyCycle(100-i)
			time.sleep(0.02)
except KeyboardIterrupt:
	pass

p.stop()

GPIO.cleanup()
