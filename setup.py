#!/usr/bin/env python2

import os
import sys
from distutils.core import setup

BASE_LOCATION = os.path.abspath(os.path.dirname(__file__))

VERSION_FILE = 'VERSION'
REQUIRES_FILE = 'REQUIREMENTS'

def filter_comments(fd):
    return filter(lambda l: l.strip().startswith("#") is False, fd.readlines())

def readfile(filename, func):
    try:
        with open(os.path.join(BASE_LOCATION, filename)) as f:
            data = func(f)
    except (IOError, IndexError):
        sys.stderr.write(u"""
Can't find '%s' file. This doesn't seem to be a valid release.

If you are working from a git clone, run:
    make describe
    setup.py develop

To build a valid release, run:
    make all

""" % filename)
        sys.exit(1)
    return data

def get_version():
    return readfile(VERSION_FILE, lambda f: f.read().strip())

def get_requires():
    return readfile(REQUIRES_FILE, filter_comments)

setup(
    name='sia',
    version=get_version(),
    description='Simple ical aggregator.',
    author='Michael Mueller',
    author_email='world@nfzd.net',
    url='http://www.github.com/nfzd/sia',
    license='GPLv2',
    #packages=['sia'],
    scripts=['bin/pitchfreq'],
    install_requires=get_requires(),
)
