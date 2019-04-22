#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import time
import datetime
import threading


class HD44780:

    def __init__(self, pin_rs=11, pin_e=10, pins_db=[5,6,7,8]):
        
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        GPIO.setmode(GPIO.BCM)
        sleep(0.1)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
	GPIO.setup(16,GPIO.OUT)
	GPIO.setup(24,GPIO.OUT)
	sleep(0.1)

        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Reset LCD """
        self.cmd(0x33) 
        self.cmd(0x32) 
        self.cmd(0x28) 
        self.cmd(0x0C) 
        self.cmd(0x06) 
        self.cmd(0x01) 
        
    def cmd(self, bits, char_mode=False):
        """ Command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)
        
        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)
        
    def message(self, text):
        """ Send string to LCD """
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)
on=26
armed=19
GPIO.setmode(GPIO.BCM)
GPIO.setup(on,GPIO.OUT)
GPIO.setup(armed,GPIO.OUT)

class budz(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		GPIO.output(16,True)
		state=0
		try:		
			for i in range(10):
				for x in range(4):
					GPIO.output(24,True)
					sleep(0.1)
					GPIO.output(24,False)
					sleep(0.1)	
				lcd.message("\n !!!BUDZENIE!!!")		
				sleep(0.5)
				lcd.message("\n BUDZENIE")
				sleep(0.5)
			while 1:
				if state == 0:
					p.ChangeDutyCycle(100)
					state=1
				else:
					p.ChangeDutyCycle(0)
					state=0
				sleep(0.5)
		except KeyboardInterrupt:
			GPIO.clear()

if __name__ == '__main__':
    GPIO.setwarnings(False)
    lcd = HD44780()
    GPIO.output(16,False)
    GPIO.output(on,True)
    tBudz='19:00:00'
    p=GPIO.PWM(armed,50)
    p.start(0)
    state=0
    try:
	    while 1:
		lcd.clear()
		t=datetime.datetime.now().strftime('%H:%M:%S')
		lcd.message(t)
		if t==tBudz:
			budz().start()
		sleep(0.9)
    except KeyboardInterrupt:
	lcd.clear()
	GPIO.cleanup()


