# PiOSCBox

Follow the instructions here https://www.instructables.com/PiOSCBOX/ for the hardware build.

Patches and scripts for a Raspberry Pi - based synth and effects processor.  
Python (rpi.gpio), C (wiringPi) and Pure Data

This repo should be cloned to the following location:

/home/pi/PiOSCBox/

After cloning to a directory on your PI Linux installation, run the build script. This will compile the rotary encoder components. External dependencies are WiringPI and Liblo. I don't remember, but I think both are already installed if you're running noobs.

Install Pure Data: https://puredata.info/docs/raspberry-pi

Copy the scripts located at /home/pi/PiOSCBox/etc/init.d/ to the system init directory /etc/init.d

Make links to the default runlevel:

ln -s /etc/init.d/box_display /etc/rc3.d/S04box_display

ln -s /etc/init.d/encoders /etc/rc3.d/S03encoders

ln -s /etc/init.d/pd-main-patch /etc/rc3.d/S05pd-main-patch


