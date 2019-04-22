#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep, time


GPIO.setmode(GPIO.BCM)


class HD44780:
    
    def __init__(self, pin_rs=11, pin_e=10, pins_db=[4,5,6,7], pin_backlight=26):
        
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
	self.pin_backlight=pin_backlight
	self.led=19

        
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
	GPIO.setup(self.pin_backlight, GPIO.OUT)
	GPIO.setup(self.led, GPIO.OUT)

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
	GPIO.output(self.pin_backlight,True)
	GPIO.output(self.led,True)
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)
	#sleep(1)
	#GPIO.output(self.pin_backlight,False)
	#GPIO.output(self.led,False)
    def reading(self, sensor):
	trigger = 21
 	echo = 12 	#obowiazkowo rezystor 1k (na 1.2k tez dziala)
	if sensor == 0:
		# GPIO output = the pin that's connected to "Trig" on the sensor
		# GPIO input = the pin that's connected to "Echo" on the sensor
	    GPIO.setup(trigger,GPIO.OUT)
	    GPIO.setup(echo,GPIO.IN)
	    GPIO.output(trigger, GPIO.LOW)
		
		# found that the sensor can crash if there isn't a delay here
		# no idea why. If you have odd crashing issues, increase delay
	    sleep(0.3)
		
		# sensor manual says a pulse ength of 10Us will trigger the 
		# sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
		# wait for the reflected ultrasonic burst to be received
		
		# to get a pulse length of 10Us we need to start the pulse, then
		# wait for 10 microseconds, then stop the pulse. This will 
		# result in the pulse length being 10Us.
		
		# start the pulse on the GPIO pin 
		# change this value to the pin you are using
		# GPIO output = the pin that's connected to "Trig" on the sensor
	    GPIO.output(trigger, True)
		
		# wait 10 micro seconds (this is 0.00001 seconds) so the pulse
		# length is 10Us as the sensor expects
	    sleep(0.00001)
		
		# stop the pulse after the time above has passed
		# change this value to the pin you are using
		# GPIO output = the pin that's connected to "Trig" on the sensor
	    GPIO.output(trigger, False)

		# listen to the input pin. 0 means nothing is happening. Once a
		# signal is received the value will be 1 so the while loop
		# stops and has the last recorded time the signal was 0
		# change this value to the pin you are using
		# GPIO input = the pin that's connected to "Echo" on the sensor
	    while GPIO.input(12) == 0:
	      signaloff = time()
		
		# listen to the input pin. Once a signal is received, record the
		# time the signal came through
		# change this value to the pin you are using
		# GPIO input = the pin that's connected to "Echo" on the sensor
	    while GPIO.input(echo) == 1:
	      signalon = time()
		
		# work out the difference in the two recorded times above to 
		# calculate the distance of an object in front of the sensor
	    timepassed = signalon - signaloff
		
		# we now have our distance but it's not in a useful unit of
		# measurement. So now we convert this distance into centimetres
	    distance = timepassed * 17000
		
		# return the distance of an object in front of the sensor in cm
	    return distance
		
		# we're no longer using the GPIO, so tell software we're done
	    GPIO.cleanup()

	else:
	    print "Incorrect usonic() function varible."
def buzz(e):
	if e == "on":	
		GPIO.output(buzzCh, True)
		GPIO.output(warnCh, True)
	else:
		GPIO.output(buzzCh,False)
		GPIO.output(warnCh,False)
buzzCh = 23
GPIO.setup(buzzCh,GPIO.OUT)
warnCh = 22
GPIO.setup(warnCh,GPIO.OUT)
if __name__ == '__main__':

    lcd = HD44780()
    buzzState=0
    print("test")
    while 1:
    	#lcd.clear()
	dist = lcd.reading(0)
    	lcd.message("Distance:\n"+str(dist)[:4]+"cm           ")
	if dist<10.0 and buzzState==0:
		buzz("on")
		buzzState=1
	elif dist>=10.0 and buzzState==1:
		buzz("off")
		buzzState=0
	sleep(0.5)
