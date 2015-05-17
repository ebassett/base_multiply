#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base_multiply - 2014-10-12 - ejb
__version__ = '0.1'
'''
Revision history
0.1 Initial version
'''


from __future__ import print_function
import argparse
from base_addition import base_addition
import sys


DIGITS = '0123456789ABCDEF'


def parse_args():
    parser = argparse.ArgumentParser(description="Multiply two numbers in a given base (default 10).")
    parser.add_argument("input_x", type=str, metavar="x", help="first  multiplicand")
    parser.add_argument("input_y", type=str, metavar="y", help="second multiplicand")
    parser.add_argument("-b", "--base", type=int, dest="base", choices=xrange(2, 17), default=10, help="base (2-16); default = %(default)s")
    parser.add_argument('--version', action='version', version='%(prog)s v' + str(__version__))
    parser.add_argument("--debug", "--verbose", action="store_true", dest="debug", help="enable debugging output")
    return parser.parse_args()



def log_debug(debug_str):
    if debug:
        print("DEBUG: ", debug_str)

def log_error(error_str):
    # EJB: I originally had 'print >> sys.stderr, "ERROR: ", error_str' here
    #       and it was getting buffered, even followed by sys.stderr.flush().
    sys.stderr.write("ERROR: %s.\n" % error_str)


if __name__ == "__main__":
    args = parse_args()
    debug = args.debug
    log_debug(args)

    base = args.base
    digits = DIGITS[0:base]
    log_debug('base: %s' % base)

    input_x = args.input_x
    input_y = args.input_y
    log_debug('x: %s' % input_x)
    log_debug('y: %s' % input_y)
    x = input_x[::-1]  # Reverse string so we can do right-to-left processing left-to-right
    y = input_y[::-1]
    log_debug('x reversed: %s' %x)
    log_debug('y reversed: %s' %y)

    # TODO: Validate that input digits are valid in given base

    products = []
    for y_digit in y:
        out_str = ''
        carry_in = 0
        for x_digit in x:
            (carry_out, output) = divmod(digits.index(x_digit) * digits.index(y_digit), base)
            output += carry_in
            if output >= base:
                (carry_out, output) = divmod(output, base)
            assert(output < base)
            out_str = '%s%s' % (digits[output], out_str)
            carry_in = carry_out
        if carry_out:
            out_str = '%s%s' % (digits[carry_out], out_str)
        products.append('%s%s' % (out_str, '0' * len(products)))
    answer = 0
    for product in products:
        answer = base_addition(base=base, x=answer, y=product)

    print('Answer: %s' % answer)
