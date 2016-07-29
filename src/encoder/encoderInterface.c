/*
 *  Copyright (C) 2016 Star Morin
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as
 *  published by the Free Software Foundation; either version 2.1 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  $Id$
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wiringPi.h>
#include "lo/lo.h"

#include "rotaryencoder.h"

int main(int argc, char *argv[])
{

// for lo sockets
//    lo_address t = lo_address_new_from_url( "osc.unix://localhost/tmp/mysocket" );

// +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
// | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
// +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
// |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
// |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
// |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
// |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 0 | IN   | TxD     | 15  | 14  |
// |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
// |  17 |   0 | GPIO. 0 |   IN | 1 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
// |  27 |   2 | GPIO. 2 |   IN | 1 | 13 || 14 |   |      | 0v      |     |     |
// |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
// |     |     |    3.3v |      |   | 17 || 18 | 1 | OUT  | GPIO. 5 | 5   | 24  |
// |  10 |  12 |    MOSI |   IN | 1 | 19 || 20 |   |      | 0v      |     |     |
// |   9 |  13 |    MISO |   IN | 1 | 21 || 22 | 1 | IN   | GPIO. 6 | 6   | 25  |
// |  11 |  14 |    SCLK |   IN | 1 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
// |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
// |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
// |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
// |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 1 | IN   | GPIO.26 | 26  | 12  |
// |  13 |  23 | GPIO.23 |   IN | 1 | 33 || 34 |   |      | 0v      |     |     |
// |  19 |  24 | GPIO.24 |   IN | 1 | 35 || 36 | 1 | IN   | GPIO.27 | 27  | 16  |
// |  26 |  25 | GPIO.25 |   IN | 1 | 37 || 38 | 0 | OUT  | GPIO.28 | 28  | 20  |
// |     |     |      0v |      |   | 39 || 40 | 0 | OUT  | GPIO.29 | 29  | 21  |
// +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
// | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
// +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+


    wiringPiSetup();

    lo_address t = lo_address_new(NULL, "9000");

    int pin_a = 22;
    int pin_b = 26;

    int pin_c = 3;
    int pin_d = 4;

    int pin_e = 25;
    int pin_f = 0;

    int pin_g = 23;
    int pin_h = 24;

    int pin_i = 2;
    int pin_j = 16;

    int pin_k = 1;
    int pin_l = 15;

    volatile long last_enc_1 = 0;
    volatile long last_enc_2 = 0;
    volatile long last_enc_3 = 0;
    volatile long last_enc_4 = 0;
    volatile long last_enc_5 = 0;
    volatile long last_enc_6 = 0;

    struct encoder *encoder1 = setupencoder(pin_a, pin_b);
    struct encoder *encoder2 = setupencoder(pin_c, pin_d);
    struct encoder *encoder3 = setupencoder(pin_e, pin_f);
    struct encoder *encoder4 = setupencoder(pin_g, pin_h);
    struct encoder *encoder5 = setupencoder(pin_i, pin_j);
    struct encoder *encoder6 = setupencoder(pin_k, pin_l);

	while (1) {
		delay(10);
		if (encoder1->value != last_enc_1) {
			last_enc_1 = encoder1->value;
			if (lo_send(t, "/enc/1/value", "i", last_enc_1) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
		if (encoder2->value != last_enc_2) {
			last_enc_2 = encoder2->value;
			if (lo_send(t, "/enc/2/value", "i", last_enc_2) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
		if (encoder3->value != last_enc_3) {
			last_enc_3 = encoder3->value;
			if (lo_send(t, "/enc/3/value", "i", last_enc_3) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
		if (encoder4->value != last_enc_4) {
			last_enc_4 = encoder4->value;
			if (lo_send(t, "/enc/4/value", "i", last_enc_4) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
		if (encoder5->value != last_enc_5) {
			last_enc_5 = encoder5->value;
			if (lo_send(t, "/enc/5/value", "i", last_enc_5) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
		if (encoder6->value != last_enc_6) {
			last_enc_6 = encoder6->value;
			if (lo_send(t, "/enc/6/value", "i", last_enc_6) == -1) {
				printf("OSC error %d: %s\n", lo_address_errno(t), lo_address_errstr(t));
			}
		}
	}

//    } else {
        /* send a message to /foo/bar with two float arguments, report any
         * errors */
//        if (lo_send(t, "/foo/bar", "ff", 0.12345678f, 23.0f) == -1) {
//            printf("OSC error %d: %s\n", lo_address_errno(t),
//                   lo_address_errstr(t));
//        }

        /* send a message to /a/b/c/d with a mixtrure of float and string
         * arguments */
//        lo_send(t, "/a/b/c/d", "sfsff", "one", 0.12345678f, "three",
//                -0.00000023001f, 1.0);

        /* send a jamin scene change instruction with a 32bit integer argument */
//        lo_send(t, "/jamin/scene", "i", 2);
//    }

    return 0;
}

/* vi:set ts=8 sts=4 sw=4: */
