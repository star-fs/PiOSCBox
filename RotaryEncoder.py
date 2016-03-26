#!/usr/bin/env python
#
# Raspberry Pi Rotary Encoder Class
# $Id: rotary_class.py,v 1.2 2014/01/14 07:30:07 bob Exp $
#
# Author : Bob Rathbone
# Site : http://www.bobrathbone.com
#
# This class uses standard rotary encoder with push switch
#
#

import RPi.GPIO as GPIO

class RotaryEncoder:
	CLOCKWISE=1
	ANTICLOCKWISE=2
	BUTTONDOWN=3
	BUTTONUP=4
	rotary_a = 0 
	rotary_b = 0 
	rotary_c = 0 
	last_state = 0 
	last_delta = 0
	direction = 0 
	stack = list()

	# Initialise rotary encoder object
	def __init__(self,pinA,pinB,button,callback):
		self.pinA = pinA
		self.pinB = pinB
		self.button = button
		self.callback = callback
		GPIO.setmode(GPIO.BCM)

		# The following lines enable the internal pull-up resistors
		# on version 2 (latest) boards
		GPIO.setwarnings(False)
		GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		#GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		if self.button != 0:
			GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		#GPIO.setup(self.button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# For version 1 (old) boards comment out the above four lines
		# and un-comment the following 3 lines
		#GPIO.setup(self.pinA, GPIO.IN)
		#GPIO.setup(self.pinB, GPIO.IN)
		#GPIO.setup(self.button, GPIO.IN)
		# Add event detection to the GPIO inputs
		GPIO.add_event_detect(self.pinA, GPIO.FALLING, callback=self.switch_event)
		GPIO.add_event_detect(self.pinB, GPIO.FALLING, callback=self.switch_event)
		if self.button != 0:
			GPIO.add_event_detect(self.button, GPIO.BOTH, callback=self.button_event, bouncetime=150)
		return

	# Call back routine called by switch events
	def switch_event(self,switch):

		totals = {1:0, 2:0, 3:0}
		event = 0
		self.rotary_a = GPIO.input(self.pinA)
		self.rotary_b = GPIO.input(self.pinB)
		new_state = (self.rotary_a ^ self.rotary_b) |self.rotary_b << 1

		if new_state != self.last_state:
			delta = (new_state -self.last_state) % 4

			print "delta:" + str(delta)

			self.stack.append(delta)
			if len(self.stack) > 10:
				self.stack.pop(0)

			for i in self.stack:
				totals[i] += 1
				
			if delta == 1 and totals[delta] > 4:
				print "clockwise"
				self.direction = self.CLOCKWISE
				event = self.direction

			elif delta == 3 and totals[delta] > 4:
				print "anticlockwise"
				self.direction = self.ANTICLOCKWISE
				event = self.direction

			elif delta == 2:

				if self.direction == self.CLOCKWISE:
					print "clockwise"
				else: 
					print "anticlockwise"
				# we don't append 2's to the stack
				event = self.direction

			self.last_state = new_state

#		self.rotary_c = self.rotary_a ^ self.rotary_b
#		new_state = self.rotary_a * 4 + self.rotary_b * 2 + self.rotary_c * 1 
#		delta = (new_state - self.last_state) % 4 
#		self.last_state = new_state
#		event = 0 

#		print "new_state:" + str(new_state)
#		print "delta:" + str(delta)

#		if delta == 1:
#			if self.direction == self.CLOCKWISE:
#				# print "Clockwise"
#				event = self.direction
#			else:
#				self.direction = self.CLOCKWISE
#		elif delta == 3:
#			if self.direction == self.ANTICLOCKWISE:
#				# print "Anticlockwise"
#				event = self.direction
#			else:
#				self.direction = self.ANTICLOCKWISE

		if event > 0:
			self.callback(event)
			return

	# Push button event
	def button_event(self,button):
		if GPIO.input(button):
			event = self.BUTTONUP
		else:
			event = self.BUTTONDOWN
			self.callback(event)
			#return

	# Get a switch state
	def getSwitchState(self, switch):
		return GPIO.input(switch)

# End of RotaryEncoder class
