/*
 *  Copyright (C) 2004 Steve Harris, Uwe Koloska
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
#include "lo/lo.h"

#include "rotaryencoder.h"

const char testdata[6] = "ABCDE";

int main(int argc, char *argv[])
{
    /* an address to send messages to. sometimes it is better to let the server
     * pick a port number for you by passing NULL as the last argument */
//    lo_address t = lo_address_new_from_url( "osc.unix://localhost/tmp/mysocket" );
    lo_address t = lo_address_new(NULL, "9000");
    lo_address t2 = lo_address_new(NULL, "9001");

    int pin_a = 6;
    int pin_b = 12;

    int pin_c = 22;
    int pin_d = 23;

    int pin_e = 26;
    int pin_f = 17;

    int pin_g = 13;
    int pin_h = 19;

    int pin_i = 27;
    int pin_j = 15;

    int pin_k = 18;
    int pin_l = 14;


//    if (argc > 1 && argv[1][0] == '-' && argv[1][1] == 'q') {
        /* send a message with no arguments to the path /quit */
        if (lo_send(t, "/quit", NULL) == -1) {
            printf("OSC error %d: %s\n", lo_address_errno(t),
                   lo_address_errstr(t));
        }
//    } else {
        /* send a message to /foo/bar with two float arguments, report any
         * errors */
        if (lo_send(t, "/foo/bar", "ff", 0.12345678f, 23.0f) == -1) {
            printf("OSC error %d: %s\n", lo_address_errno(t),
                   lo_address_errstr(t));
        }
        if (lo_send(t, "/foo/bar", "ff", 0.12345678f, 23.0f) == -1) {
            printf("OSC error %d: %s\n", lo_address_errno(t),
                   lo_address_errstr(t));
        }

        /* send a message to /a/b/c/d with a mixtrure of float and string
         * arguments */
        lo_send(t, "/a/b/c/d", "sfsff", "one", 0.12345678f, "three",
                -0.00000023001f, 1.0);

        /* send a 'blob' object to /a/b/c/d */
        lo_send(t, "/a/b/c/d", "b", btest);

        /* send a jamin scene change instruction with a 32bit integer argument */
        lo_send(t, "/jamin/scene", "i", 2);
//    }

    return 0;
}

/* vi:set ts=8 sts=4 sw=4: */
