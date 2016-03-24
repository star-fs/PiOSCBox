#!/usr/bin/python

import sys
import time
#import Adafruit_SSD1306
#
#import Image
#import ImageDraw
#import ImageFont

from RotaryEncoder import RotaryEncoder

import liblo

PIN_A = 6
PIN_B = 12

PIN_C = 22
PIN_D = 23

PIN_E = 18
PIN_F = 17

PIN_G = 9
PIN_H = 7

PIN_I = 27
PIN_J = 15

PIN_K = 4 
PIN_L = 14

values = {
	1: 0,
	2: 0,
	3: 0,
	4: 0,
	5: 0,
	6: 0
}

RST=0

target = liblo.Address(9001)
target2 = liblo.Address(9000)

def rot_event_1(event):
	update_values(event, 1)

def rot_event_2(event):
	update_values(event, 2)

def rot_event_3(event):
	update_values(event, 3)

def rot_event_4(event):
	update_values(event, 4)

def rot_event_5(event):
	update_values(event, 5)

def rot_event_6(event):
	update_values(event, 6)

def update_values(event, enc):
	if event == RotaryEncoder.CLOCKWISE:
		values[enc] = values[enc] + 1
		update_display(enc)

	elif event == RotaryEncoder.ANTICLOCKWISE:
		values[enc] = values[enc] - 1
		update_display(enc)

def update_display(enc_number):
	global client
	global values
	global fifo_out

#	if (enc_number == 3):
#		values[enc_number] = values[enc_number] * -1

#	if (enc_number == 4):
#		values[enc_number] = values[enc_number] * -1

#	if (enc_number == 6):
#		values[enc_number] = values[enc_number] * -1

	liblo.send( target, "/enc/" + str(enc_number), values[enc_number] )
#	liblo.send( target2, "/enc/" + str(enc_number), values[enc_number] )
	print("/enc/" + str(enc_number) + ":" + str(values[enc_number]))
	#fifo_out.write( "/enc/" + str(enc_number) + ":" + str(values[enc_number]) + "\n" )
	#fifo_out.flush()

rot1 = RotaryEncoder(PIN_A,PIN_B, 0,rot_event_1)
rot2 = RotaryEncoder(PIN_C,PIN_D, 0,rot_event_2)
rot3 = RotaryEncoder(PIN_E,PIN_F, 0,rot_event_3)
rot4 = RotaryEncoder(PIN_G,PIN_H, 0,rot_event_4)
rot5 = RotaryEncoder(PIN_I,PIN_J, 0,rot_event_5)
rot6 = RotaryEncoder(PIN_K,PIN_L, 0,rot_event_6)

while True:
	# do stuff
	#time.sleep(0.0025)
	pass
	
