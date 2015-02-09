#!/usr/bin/env python2

import argparse
import math
import os
import re
import sys


def exit(error_msg):
    sys.exit(os.path.basename(__file__) + ": Error: " + error_msg)

def a4diff(base, octave, nflat, nsharp):
    """Compute the number of half-tones difference to A4."""
    n = {
            'a': 0,
            'b': 2,
            'c': -9,
            'd': -7,
            'e': -5,
            'f': -4,
            'g': -2
        }.get(base)

    n += 12 * (octave - 4)
    n -= nflat
    n += nsharp

    return n


parser = argparse.ArgumentParser(description='Convert various pitch and frequency representations using equal temperament.')
parser.add_argument(dest='string', type=str, help='Input, by default either frequency or scientific pitch notation is assumed.')
parser.add_argument('-m', dest='helmholtz', action='store_true', default=False, help='Pitch is in Helmholtz notation / musical notation.')
parser.add_argument('-a', dest='showall', action='store_true', default=False, help='Show all notations.')
parser.add_argument('-t', dest='tuning', action='store', default=440, help='Tuning of A4 (default: 440)')
#parser.add_argument('-c', dest='speedofsound', action='store', default=434, help='Speed of sound (default: 434)')

args = parser.parse_args()

s = args.string
helmholtz = args.helmholtz
showall = args.showall
tuning = args.tuning
#c = args.speedofsound

if showall:
    exit("-a NOT IMPLEMENTED")
    # TODO


freq = True

try:
    f = float(s)

    if math.isnan(f) or math.isinf(f) or f == 0.0:
        freq = False

except ValueError:
    freq = False


if freq:
    exit("freq NOT IMPLEMENTED")
    # TODO

else:
    if not helmholtz:

        # check for bad chars

        if re.search('[^0-9a-gA-G#]', s):
            exit("Bad character in scientic pitch notation.")


        # split number and other chars

        l, cl = re.subn('[0-9]+', '', s)
        n, cn = re.subn('[a-gA-G#]+', '', s)

        if cl < 1 or cn != 1:
            exit("Bad format for scientic pitch notation: can't find note and octave.")


        # process number

        try:
            o = int(n)
        except ValueError:
            exit("Bad format for scientic pitch notation: can't parse octave number.")


        # process note

        l = l.lower()

        nflat = l.count('b')
        nsharp = l.count('#')

        l = re.sub('[b#]', '', l)

        if l == "":
            # removed one b too much, b is base note
            if nflat < 1:
                exit("Bad format for scientic pitch notation: no note found.")

            nflat -= 1
            l = 'b'

        if nflat > 2 or nsharp > 2:
            exit("Bad format for scientic pitch notation: too many # or b.")

        if nflat > 0 and nsharp > 0:
            exit("Bad format for scientic pitch notation: mixing # and b.")

        base = l
        octave = o

    else:
        # check for bad chars

        if re.search("[^1-9a-gA-G#,']", s):
            exit("Bad character in helmholtz notation.")


        # split number and other chars

        l, cl = re.subn("[1-9,']+", '', s)
        n, cn = re.subn('[a-gA-G#]+', '', s)

        if cl < 1 or cn != 1:
            exit("Bad format for helmholtz notation: can't find note and octave.")


        # process numbering

        nticks = n.count("'")
        ncommas = n.count(",")

        n = re.sub("[',]*", '', n)

        if nticks > 0 and ncommas > 0:
            exit("Bad format for scientic pitch notation: mixing ticks and commas.")

        if (nticks > 0 or ncommas > 0) and n != "":
            exit("Bad format for scientic pitch notation: mixing ticks or commas with numbers.")

        if nticks == 0 and ncommas == 0 and n != "":
            o = 0

            if n != "":
                try:
                    o = int(n)
                except ValueError:
                    exit("Bad format for helmholtz notation: can't parse octave number.")


        # process note

        nflat = l.count('b')
        nsharp = l.count('#')

        l = re.sub('[b#]', '', l)

        if l == "":
            # removed one b too much, b is base note
            if nflat < 1:
                exit("Bad format for helmholtz notation: no note found.")

            nflat -= 1
            l = 'b'

        if nflat > 2 or nsharp > 2:
            exit("Bad format for helmholtz notation: too many # or b.")

        if nflat > 0 and nsharp > 0:
            exit("Bad format for helmholtz notation: mixing # and b.")

        if l.islower():
            octave = 3

            if ncommas > 0:
                exit("Bad format for helmholtz notation: mixing upper-case note and commas.")

            if nticks > 0:
                octave += nticks
            else:
                octave += o
        else:
            octave = 2

            if nticks > 0:
                exit("Bad format for helmholtz notation: mixing upper-case note and ticks.")

            if ncommas > 0:
                octave -= ncommas
            else:
                octave -= o

        base = l.lower()

    n = a4diff(base, octave, nflat, nsharp)
    a = math.pow(2, 1/12.)
    f = tuning * (a**n)

    print "Frequency: {0:.3f}".format(f)