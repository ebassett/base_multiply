#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base_multiply - 2014-10-12 - ejb

from __future__ import print_function
import argparse
from base_addition import base_addition
import sys


__version__ = '0.1'
'''
Revision history
0.1 Initial version
'''


DIGITS = '0123456789ABCDEF'
debug = False


def parse_args():
    parser = argparse.ArgumentParser(description="Multiply two numbers in a given base (default 10).")
    parser.add_argument("-b", "--base", type=int, dest="base", choices=xrange(2, 17), default=10, help="base (2-16); default = %(default)s")
    parser.add_argument("multiplicands", type=str, metavar="NUM", nargs='+', help="first  multiplicand")
    parser.add_argument('--version', action='version', version='%(prog)s v' + str(__version__))
    parser.add_argument("--debug", "--verbose", action="store_true", dest="debug", help="enable debugging output")
    return parser.parse_args()



def log_debug(debug_str):
    if debug:
        print("DEBUG (mulitply): ", debug_str)

def log_error(error_str):
    # EJB: I originally had 'print >> sys.stderr, "ERROR: ", error_str' here
    #       and it was getting buffered, even followed by sys.stderr.flush().
    sys.stderr.write("ERROR: {}.\n".format(error_str))

def base_multiply(debug, base, multiplicands):
    digits = DIGITS[0:base]
    accumulator = 1  # Multiplicative identity

    log_debug('base: {}'.format(base))
    log_debug('multiplicands: {}'.format(multiplicands))

    if len(multiplicands) == 1:
        return multiplicands.pop()
    else:
        accumulator = multiplicands.pop()

    while len(multiplicands) > 0:
        input_x = accumulator
        input_y = multiplicands.pop()


        log_debug('x: {}'.format(input_x))
        log_debug('y: {}'.format(input_y))
        x = input_x[::-1]  # Reverse string so we can do right-to-left processing left-to-right
        y = input_y[::-1]
        log_debug('x reversed: {}'.format(x))
        log_debug('y reversed: {}'.format(y))

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
                out_str = '{}{}'.format(digits[output], out_str)
                carry_in = carry_out
            if carry_out:
                out_str = '{}{}'.format(digits[carry_out], out_str)
            products.append('{}{}'.format(out_str, '0' * len(products)))
        answer = 0
        for product in products:
            accumulator = base_addition(debug=debug, base=base, x=answer, y=product)

    return accumulator


if __name__ == "__main__":
    args = parse_args()
    debug = args.debug
    log_debug(args)

    base = args.base
    multiplicands = args.multiplicands

    answer = base_multiply(debug=debug, base=base, multiplicands=multiplicands)
    print('Answer: {}'.format(answer))
