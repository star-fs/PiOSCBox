#!/usr/bin/python

import time
import liblo
import sys

sys.path.append("../lib/python/st7562/")

import st7565

import xglcd_font as font
fixed = font.XglcdFont('../lib/python/st7562/fonts/Wendy7x8.c', 7, 8)
neato = font.XglcdFont('../lib/python/st7562/fonts/FixedFont5x8.c', 5, 8)

#neato = font.XglcdFont('../lib/python/st7562/fonts/Neato5x7.c', 5, 7)
#wendy_font = font.XglcdFont('../lib/python/st7562/fonts/ArcadePix9x11.c', 9, 11)
#wendy_font = font.XglcdFont('../lib/python/st7562/fonts/Robotron7x11.c', 7, 11)
#wendy_font = font.XglcdFont('../lib/python/st7562/fonts/Bally7x9.c', 7, 9)

glcd = st7565.Glcd(rgb=[21,20,16])
glcd.init()
glcd.set_backlight_color(100, 100, 2)

from netifaces import interfaces, ifaddresses, AF_INET

#ifaceName = 'eth0'
ifaceName = 'wlan0'
ip_addrs  = ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'no ip'}] )

ip_addr = ip_addrs[0]['addr']

if len(ip_addr) == 0:
	ip_addrs  = ifaddresses('eth0').setdefault(AF_INET, [{'addr':'no ip'}] )
	ip_addr = ip_addrs[0]['addr']
	ip_addr = ip_addrs[0]['addr']

server = liblo.Server(9001)

RST=0

global_count = 0

width = 128
height = 64

values = {
	"/enc/1/value": 0,
	"/enc/1/label": "PatSel",
	"/enc/2/value": 0,
	"/enc/2/label": "ctr2",
	"/enc/3/value": 0,
	"/enc/3/label": "ctr3",
	"/enc/4/value": 0,
	"/enc/4/label": "ctl4",
	"/enc/5/value": 0,
	"/enc/5/label": "ctl5",
	"/enc/6/value": 0,
	"/enc/6/label": "ctl6",
	"/patch_name": "default",
	"/global/dispval": 0,
	#"enc6": {"value": 0,"name": "ctrl 6"},
}

def update_display(path, args, types, source):

	global glcd
	global wendy_font

	global width
	global height

	global global_count

	if types[0] == "i":
		values[path] = int(args[0])

	elif types[0] == "s":
		values[path] = str(args[0])
		
# main

server.add_method( "/enc/1/value", "i", update_display)
server.add_method( "/enc/1/label", "s", update_display)
server.add_method( "/enc/2/value", "i", update_display)
server.add_method( "/enc/2/label", "s", update_display)
server.add_method( "/enc/3/value", "i", update_display)
server.add_method( "/enc/3/label", "s", update_display)
server.add_method( "/enc/4/value", "i", update_display)
server.add_method( "/enc/4/label", "s", update_display)
server.add_method( "/enc/5/value", "i", update_display)
server.add_method( "/enc/5/label", "s", update_display)
server.add_method( "/enc/6/value", "i", update_display)
server.add_method( "/enc/6/label", "s", update_display)

server.add_method( "/global/dispval", "i", update_display)

while True:

	global_count += 1

	server.recv(100)

	# update display
	if (global_count - 3 > 1):

		glcd.clear_back_buffer()
		glcd.draw_rectangle(0, 0, 128, 64)

		# row 1 lables
		glcd.draw_string(str("PATCH"), fixed, 5, 3,spacing=0)
		glcd.draw_string(str(values["/enc/2/label"]), fixed, 55, 3,spacing=0)
		glcd.draw_string(str(values["/enc/3/label"]), fixed, 95, 3,spacing=0)

		# row 1 values
		glcd.draw_string(str(values["/enc/1/value"]), neato, 5, 14,spacing=0)
		glcd.draw_string(str(values["/enc/2/value"]), neato, 55, 14,spacing=0)
		glcd.draw_string(str(values["/enc/3/value"]), neato, 95, 14,spacing=0)

		# row 2 lables
		glcd.draw_string(str(values["/enc/4/label"]), fixed, 5, 26,spacing=0)
		glcd.draw_string(str(values["/enc/5/label"]), fixed, 55, 26,spacing=0)
		glcd.draw_string(str(values["/enc/6/label"]), fixed, 95, 26,spacing=0)

		# row 2 values
		glcd.draw_string(str(values["/enc/4/value"]), neato, 5, 38,spacing=0)
		glcd.draw_string(str(values["/enc/5/value"]), neato, 55, 38,spacing=0)
		glcd.draw_string(str(values["/enc/6/value"]), neato, 95, 38,spacing=0)

		# general info
		glcd.draw_string(ip_addr + "::->" + str(values["/enc/1/label"]), fixed, 7, 55,spacing=0)
		glcd.draw_string("-->" + str(values["/global/dispval"]), fixed, 90, 55,spacing=0)

		glcd.flip()
		#disp.display()
		global_count = 0
