#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import os
import time


class HD44780:

    def __init__(self, pin_rs=11, pin_e=10, pins_db=[5,6,7,8]):
        
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)

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
def read_temp_raw():
	f=open(temp_sensor,'r')
	lines=f.readlines()
	f.close()
	return lines

def read_temp():
	lines=read_temp_raw()
	while lines[0].strip()[-3:]!='YES':
		time.sleep(0.2)
		lines=read_temp_raw()
	temp_o=lines[1].find('t=')
	if temp_o!=-1:
		temp_string=lines[1].strip()[temp_o+2:] 
		temp_c=float(temp_string)/1000.0
		temp_f = temp_c*9.0/5.0+32.0
		return temp_c
#
#	PINs:
#	1 - GND
#	2 - digitOut -> 4,7kOhm -> 5V i rownolegle do GPIO_4 (tylko GPIO_4 obluguje 1_WIRE)
#	3 - 5V
#
if __name__ == '__main__':

    lcd = HD44780()
    lcd.clear()
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    temp_sensor='/sys/bus/w1/devices/28-000006bed364/w1_slave' 
    lcd.clear()
    sleep(0.5)

    while 1:
	lcd.message("CPC office Temp \n"+str(read_temp())+"            ")
	sleep(1)

