#servo test
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p=GPIO.PWM(18,50)
p.start(12)
try:
	while True:
		p.ChangeDutyCycle(1.5)
		time.sleep(0.5)
		p.ChangeDutyCycle(7.0)
		time.sleep(0.5)
		p.ChangeDutyCycle(12.0)
		time.sleep(0.5)
		
except KeyboardInterrupt:
	p.ChangeDutyCycle(7.0)
	time.sleep(0.1)
	GPIO.cleanup()


#p=GPIO.PWM(18,50)
#p.start(50)
#p.ChangeDutyCycle(90)
#input('press any key to stop')
#p.stop()
#GPIO.cleanup()
