pitchfreq
===

Convert various pitch and frequency notations.

Currently in alpha stage.

Pitch Notations
===

- Scientific pitch notation: octaves are numbered from zero to ten, giving notes C0 to B10 (or c0 to b10). Tuning note is A4 (usually aroung 440 Hz).
- Helmholtz / musical notation: This notation is case-sensitive. Scientific octave 3 ist the small octave, named c to b. Higher octaves are numbered according to distance (e.g. octave 4 is c1 to b1, etc.). Octave 2 is the great octave, named C to B. Lower octaves are similarly numbered according to distance (e.g. C1 to B1). Usually, ticks and commas are used: c2 = c'' and C2 = C,,
- MIDI pitch: A4 is equal to MIDI pitch 69.

Usage
===

```
pitchfreq.py [-h] [-H] [-m] [-a] [-t TUNING] string
```

- string: input. A number will be regarded as frequency and converted to a note. An alphanumerical string will be regarded as pitch notation and converted to a frequency.
- -h: display help message
- -H: use helmholtz / musical notation for input / output
- -m: input number is a midi pitch, or input note string will be converted to a midi pitch
- -t TUNING: tuning frequency for A4 if not 440 Hz
- -a: show all possible information (wavelength etc.), __IN DEVELOPMENT__

Examples
===
```
$ ./pitchfreq.py 430
Nearby notes:
A4 (frequency: 440.000)
G#4 (frequency: 415.305)

$ ./pitchfreq.py -H 510
Nearby notes:
c'' (frequency: 523.251)
b' (frequency: 493.883)

$ ./pitchfreq.py Cb0
Frequency: 15.434

$ ./pitchfreq.py -H "c##''"
Frequency: 587.330

$ ./pitchfreq.py -m 99
D#7

$ ./pitchfreq.py $(./pitchfreq.py -m 99)
Frequency: 2489.016
```
