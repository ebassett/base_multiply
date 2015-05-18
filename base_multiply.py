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
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-b", "--base", type=int, dest="base", choices=xrange(2, 17), default=10, help="base (2-16); default = %(default)s")
    group.add_argument("--multiplicands", type=str, metavar="NUM", nargs='+', help="multiplicands")
    group.add_argument("--test", action="store_true", help="run test suite")
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

def run_tests():
    pass

def base_multiply(debug, base, multiplicands):
    digits = DIGITS[0:base]
    accumulator = 1  # Multiplicative identity

    log_debug('base: {}'.format(base))
    log_debug('multiplicands: {}'.format(multiplicands))

    if not multiplicands:
        log_error('No multiplicands.')
        sys.exit(-1)

    if len(multiplicands) == 1:
        return multiplicands.pop()
    else:
        multiplicands = multiplicands[::-1]  # Reverse so we process efficiently in user-given order.
        log_debug('multiplicands: {}'.format(multiplicands))
        accumulator = multiplicands.pop()
        log_debug('accumulator: {}'.format(accumulator))

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

        partial_products = []
        final_products = []
        carry_in = 0
        for y_digit in y:
            out_str = ''
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
            partial_products.append('{}{}'.format(out_str, '0' * len(partial_products)))
        answer = 0
        log_debug('partial_products of digits: {}'.format(partial_products))
        for partial_product in partial_products:
            answer = base_addition(debug=debug, base=base, addends = [answer, partial_product])
            log_debug('sum of partial products of digits: {}'.format(answer))
        accumulator = answer
        final_products.append(answer)
        # EJB: This is wrong.
        #log_debug('accumulator before adding final answer of previous two multiplicands: {}'.format(accumulator))
        #accumulator = base_addition(debug=debug, base=base, addends = [accumulator, answer])
        #log_debug('accumulator after adding final answer of previous two multiplicands: {}'.format(accumulator))
    final_answer = 0
    for final_product in final_products:
        final_answer = base_addition(debug=debug, base=base, addends = [final_answer, final_product])

    # Ugly special-case handling for something like '000000'
    try:
        if int(final_answer) == 0:
            final_answer = '0'
    except:  # If int(_) fails because final_answer is something like 1FF, then just let it through.
        pass

    return final_answer

if __name__ == "__main__":
    args = parse_args()
    debug = args.debug
    log_debug(args)

    if args.test:
        run_tests()
    else:
        base = args.base
        multiplicands = args.multiplicands

        answer = base_multiply(debug=debug, base=base, multiplicands=multiplicands)
        print('Answer: {}'.format(answer))
