#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base_multiply - 2014-10-12 - ejb

import sys


DEBUG = True
DIGITS = '0123456789ABCDEF'


def log_debug(debug_str):
    print "DEBUG: ", debug_str

def log_error(error_str):
    # EJB: I originally had 'print >> sys.stderr, "ERROR: ", error_str' here
    #       and it was getting buffered, even followed by sys.stderr.flush().

    sys.stderr.write("ERROR: %s.\n" % error_str)


if __name__ == "__main__":
    base = 4
    digits = DIGITS[0:base]
    x = '3'
    y = '3'
    (quotient, remainder) = divmod(digits.index(x) * digits.index(y), base)
    log_debug('%s\t%s' % (quotient, remainder))



