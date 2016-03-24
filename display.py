#!/usr/bin/python

import time
import liblo

import st7565
import xglcd_font as font
wendy_font = font.XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
#wendy_font = font.XglcdFont('fonts/Wendy7x8.c', 7, 8)

glcd = st7565.Glcd(rgb=[21,20,16])
glcd.init()
#glcd.set_backlight_color(0, 100, 0)


from netifaces import interfaces, ifaddresses, AF_INET

#ifaceName = 'eth0'
ifaceName = 'wlan0'
ip_addrs  = ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )

ip_addr = ip_addrs[0]['addr']

server = liblo.Server(9001)

RST=0

global_count = 0

width = 128
height = 64

values = {
	"enc1": 0,
	"enc2": 0,
	"enc3": 0,
	"enc4": 0,
	"enc5": 0,
	"enc6": 0
}

def update_display(path, args, types, source):
	global glcd
	global wendy_font

	global width
	global height

	global global_count

	var_name = path.replace("/","")
	values[var_name] = int(args[0])
	foo_test(path, args, types, source)

def foo_test(path, args, types, source):
	var_name = path.replace("/","")
	
server.add_method( "/enc/1", "i", update_display)
server.add_method( "/enc/2", "i", update_display)
server.add_method( "/enc/3", "i", update_display)
server.add_method( "/enc/4", "i", update_display)
server.add_method( "/enc/5", "i", update_display)
server.add_method( "/enc/6", "i", update_display)

# handle all pending requests then return
while True:
	global_count = global_count + 1
	server.recv(100)

#       if (enc_number == 1):
#               values[enc_number] = values[enc_number] * -1

#       if (enc_number == 3):
#               values[enc_number] = values[enc_number] * -1

#       if (enc_number == 5):
#               values[enc_number] = values[enc_number] * -1

	#glcd.set_backlight_color(10, 100, 50)
	
	# update display
	if (global_count - 2 > 1):
		glcd.clear_back_buffer()
		glcd.draw_rectangle(0, 0, 128, 64)
		glcd.draw_string(str(values["enc1"] * -1), wendy_font, 5, 5,spacing=0)
		glcd.draw_string(str(values["enc2"] * -1), wendy_font, 55, 5,spacing=0)
		glcd.draw_string(str(values["enc3"] * -1), wendy_font, 105, 5,spacing=0)

		glcd.draw_string("ip:" + ip_addr, wendy_font, 5, 30,spacing=0)

		glcd.draw_string(str(values["enc4"]), wendy_font, 5, 50,spacing=0)
		glcd.draw_string(str(values["enc5"] * -1), wendy_font, 55, 50,spacing=0)
		glcd.draw_string(str(values["enc6"]), wendy_font, 105, 50,spacing=0)

		glcd.flip()
		#disp.display()
		global_count = 0
