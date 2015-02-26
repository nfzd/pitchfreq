#!/usr/bin/env python2

import argparse
import math
import os
import re
import sys


def _exit(error_msg):
    sys.exit(os.path.basename(__file__) + ": Error: " + error_msg)


def _getfloat(string):
    error = False

    try:
        value = float(string)

        if math.isnan(value) or math.isinf(value) or value == 0.0:
            error = True

    except ValueError:
        error = True
        value = float('nan')

    return value, error

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


def nfreq(n, tuning):
    """Give frequency for note with n half-tones difference to A4."""

    a = math.pow(2, 1/12.)
    f = tuning * (a**n)

    return f


def nnote(n, helmholtz):
    """Give the name of the note with n half-tones difference to A4."""

    octave = 0

    while abs(n) > 11 or n < 0:
        octave += math.copysign(1, n)
        n -= math.copysign(12, n)

    base = ('a', 'a#', 'b', 'c', 'c#', 'd',
            'd#','e', 'f', 'f#', 'g', 'g#')[int(n)].upper()
    octave = int(octave) + 4
    if n > 2:
        octave += 1

    if not helmholtz:
        return base + str(octave)
    else:
        octave = int(octave)

        if octave > 2:
            base = base.lower()
            octnot = "'" * (octave - 3)
        else:
            octnot = "," * (2 - octave)
        
        return base + octnot


def nmidi(n):
    return int(n + 69)


def midin(midi_pitch):
    return midi_pitch - 69


def _printall(n, tuning, c):
    _printfreq(n, tuning)
    _printlambda(n, tuning, c)
    _printmidi(n)
    _printnote(n, False)
    _printnote(n, True)


def _printfreq(n, tuning):
    f = nfreq(n, tuning)

    print "Frequency: {0:.3f} Hz".format(f)


def _printlambda(n, tuning, c):
    f = nfreq(n, tuning)
    lamb = c / f

    print "Wave length: {0:.3f} m".format(lamb)


def _printmidi(n):
    m = nmidi(n)

    print "MIDI pitch: {0:d}".format(m)


def _printnote(n, helmholtz):
    s = nnote(n, helmholtz)

    if not helmholtz:
        print "Scientific notation: " + s
    else:
        print "Helmholtz notation: " + s


def _printnotefreq(n, helmholtz, tuning):
    s = nnote(n, helmholtz)
    f = nfreq(n, tuning)
    print s + " (frequency: {0:.3f} Hz)".format(f)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert various pitch and ' \
                'frequency notations using equal temperament.')
    parser.add_argument(dest='string', type=str,help='Input, by default ' \
                'either frequency or scientific pitch notation is assumed.')
    parser.add_argument('-H', dest='helmholtz', action='store_true',
                default=False, help='Input or output uses Helmholtz ' \
                'notation / musical notation.')
    parser.add_argument('-m', dest='midi', action='store_true', default=False,
                help='Input or output is MIDI pitch.')
    parser.add_argument('-a', dest='showall', action='store_true',
                default=False, help='Show all notations.')
    parser.add_argument('-t', dest='tuning', action='store', default=440,
                type=float, help='Tuning of A4 in Hz (default: 440)')
    parser.add_argument('-c', dest='speed', action='store', type=float,
                default=343, help='Speed of sound in m/s (default: 343)')

    args = parser.parse_args()

    s = args.string
    helmholtz = args.helmholtz
    midi = args.midi
    showall = args.showall
    tuning = args.tuning

    c, error = _getfloat(args.speed)
    if error:
        _exit("Bad value for SPEED.")

    f, error = _getfloat(s)
    freq = not error

    if freq:

        if not midi:
            n = 12 * math.log((f / tuning), 2)

            nu = math.ceil(n)
            nl = math.floor(n)

            if nu == nl:
                if not showall:
                    _printnote(nu, helmholtz)
                else:
                    _printall(nu, tuning, c)
            else:
                print "Nearby notes:"

                dn = nu - n
                thres = .2

                if nu == round(n):
                    if not showall:
                        _printnotefreq(nu, helmholtz, tuning)

                        if dn > thres:
                            _printnotefreq(nl, helmholtz, tuning)
                    else:
                        _printall(nu, tuning, c)
                        print ""
                        _printall(nl, tuning, c)
                else:
                    dn = 1 - dn

                    if not showall:
                        _printnotefreq(nl, helmholtz, tuning)

                        if dn > thres:
                            _printnotefreq(nu, helmholtz, tuning)
                    else:
                        _printall(nl, tuning, c)
                        print ""
                        _printall(nu, tuning, c)

        else:
            if not f.is_integer():
                _exit("MIDI pitch must be an integer.")

            n = midin(int(f))

            if not showall:
                _printnote(n, helmholtz)
            else:
                _printall(n, tuning, c)

    else:
        if not helmholtz:

            # check for bad chars

            if re.search('[^0-9a-gA-G#]', s):
                _exit("Bad character in scientic pitch notation.")


            # split number and other chars

            l, cl = re.subn('[0-9]+', '', s)
            n, cn = re.subn('[a-gA-G#]+', '', s)

            if cl < 1 or cn != 1:
                _exit("Bad format for scientic pitch notation: can't find " \
                        "note and octave.")


            # process number

            try:
                o = int(n)
            except ValueError:
                _exit("Bad format for scientic pitch notation: can't parse " \
                        "octave number.")


            # process note

            l = l.lower()

            nflat = l.count('b')
            nsharp = l.count('#')

            l = re.sub('[b#]', '', l)

            if l == "":
                # removed one b too much, b is base note
                if nflat < 1:
                    _exit("Bad format for scientic pitch notation: no note " \
                            "found.")

                nflat -= 1
                l = 'b'

            if nflat > 2 or nsharp > 2:
                _exit("Bad format for scientic pitch notation: too many # " \
                        "or b.")

            if nflat > 0 and nsharp > 0:
                _exit("Bad format for scientic pitch notation: mixing # and " \
                        "b.")

            base = l
            octave = o

        else:
            # check for bad chars

            if re.search("[^1-9a-gA-G#,']", s):
                _exit("Bad character in helmholtz notation.")


            # split number and other chars

            l, cl = re.subn("[1-9,']+", '', s)
            n, cn = re.subn('[a-gA-G#]+', '', s)

            if cn != 1:
                _exit("Bad format for helmholtz notation: can't find note " \
                        "and octave.")


            # process numbering

            nticks = n.count("'")
            ncommas = n.count(",")

            n = re.sub("[',]*", '', n)

            if nticks > 0 and ncommas > 0:
                _exit("Bad format for helmholtz notation: mixing ticks " \
                        "and commas.")

            if (nticks > 0 or ncommas > 0) and n != "":
                _exit("Bad format for helmholtz notation: mixing ticks " \
                        "or commas with numbers.")

            if nticks == 0 and ncommas == 0:
                o = 0

                if n != "":

                    if n != "":
                        try:
                            o = int(n)
                        except ValueError:
                            _exit("Bad format for helmholtz notation: can't " \
                                    "parse octave number.")


            # process note

            nflat = l.count('b')
            nsharp = l.count('#')

            l = re.sub('[b#]', '', l)

            if l == "":
                # removed one b too much, b is base note
                if nflat < 1:
                    _exit("Bad format for helmholtz notation: no note found.")

                nflat -= 1
                l = 'b'

            if nflat > 2 or nsharp > 2:
                _exit("Bad format for helmholtz notation: too many # or b.")

            if nflat > 0 and nsharp > 0:
                _exit("Bad format for helmholtz notation: mixing # and b.")

            if l.islower():
                octave = 3

                if ncommas > 0:
                    _exit("Bad format for helmholtz notation: mixing "\
                            "upper-case note and commas.")

                if nticks > 0:
                    octave += nticks
                else:
                    octave += o
            else:
                octave = 2

                if nticks > 0:
                    _exit("Bad format for helmholtz notation: mixing " \
                            "lower-case note and ticks.")

                if ncommas > 0:
                    octave -= ncommas
                else:
                    octave -= o

            base = l.lower()

        n = a4diff(base, octave, nflat, nsharp)
        
        if showall:
            _printall(n, tuning, c)
        elif not midi:
            _printfreq(n, tuning)
        else:
            _printmidi(n)
