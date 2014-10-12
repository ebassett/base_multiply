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
    input_x = '03030'
    input_y = '3'
    x = input_x[::-1]  # Reverse string so we can to right-to-left processing left-to-right
    y = input_y[::-1]
    log_debug('x reversed: %s' %x)
    log_debug('y reversed: %s' %y)

    #(quotient, remainder) = divmod(digits.index(x) * digits.index(y), base)
    #log_debug('%s\t%s' % (quotient, remainder))

    out_str = ''

    carry_in = 0
    for x_digit in x:
        (carry_out, output) = divmod(digits.index(x_digit) * digits.index(y), base)
        output += carry_in
        if output >= base:
            (carry_out, output) = divmod(output, base)
        assert(output < base)
        out_str = '%d%s' % (output, out_str)
        carry_in = carry_out
    if carry_out:
        out_str = '%d%s' % (carry_out, out_str)

    print('Answer: %s' % out_str)





