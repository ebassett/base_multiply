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


DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
debug = False


def parse_args():
    parser = argparse.ArgumentParser(description="Multiply two numbers in a given base (default 10).")
    parser.add_argument("-b", "--base", type=int, dest="base", choices=xrange(2, 36 + 1), default=10, help="base (2-36); default = %(default)s")
    group = parser.add_mutually_exclusive_group()
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
    assert(base_multiply(debug=False, base=2,  multiplicands=[110, 1]) == '110')
    assert(base_multiply(debug=False, base=3,  multiplicands=[102, 11]) == '1122')
    assert(base_multiply(debug=False, base=3,  multiplicands=[200, 222]) == '122100')
    assert(base_multiply(debug=False, base=4,  multiplicands=[323, 212]) == '203002')
    assert(base_multiply(debug=False, base=4,  multiplicands=[212, 323]) == '203002')
    assert(base_multiply(debug=False, base=5,  multiplicands=[201, 12]) == '2412')
    assert(base_multiply(debug=False, base=5,  multiplicands=[114, 32]) == '4303')
    assert(base_multiply(debug=False, base=6,  multiplicands=[11, 13]) == '143')
    assert(base_multiply(debug=False, base=6,  multiplicands=[1001, 225]) == '225225')
    assert(base_multiply(debug=False, base=7,  multiplicands=[66, 11, 222, 0]) == '0')
    assert(base_multiply(debug=False, base=8,  multiplicands=[7, 6, 5, 4, 3, 2, 1]) == '11660')
    assert(base_multiply(debug=False, base=8,  multiplicands=[711, 5007]) == '4363177')
    assert(base_multiply(debug=False, base=9,  multiplicands=[3, 3]) == '10')
    assert(base_multiply(debug=False, base=10, multiplicands=[33333, 3]) == '99999')
    assert(base_multiply(debug=False, base=12, multiplicands=[7, 13]) == '89')
    assert(base_multiply(debug=False, base=12, multiplicands=['2B', '3A']) == 'B22')
    assert(base_multiply(debug=False, base=12, multiplicands=['3a', '2b']) == 'B22')
    assert(base_multiply(debug=False, base=16, multiplicands=['789ABC', '5DEF']) == '2C40CEC184')
    assert(base_multiply(debug=False, base=16, multiplicands=['DEAD', 'BEEF']) == 'A6144983')
    assert(base_multiply(debug=False, base=20, multiplicands=['GB', 'EB']) == 'C0G1')
    assert(base_multiply(debug=False, base=36, multiplicands=['ED', 'GAIL']) == '6HZ0VL')
    print ('All tests passed.')

def base_multiply(debug, base, multiplicands):
    digits = DIGITS[0:base]
    accumulator = 1  # Multiplicative identity

    log_debug('base: {}'.format(base))
    log_debug('multiplicands: {}'.format(multiplicands))

    # Validate that input digits are valid in given base
    valid = True
    for multiplicand in multiplicands:
        for digit in str(multiplicand).upper():
            if not str(digit).upper() in digits:
                valid = False
                log_error('Invalid number {} for base {}'.format(multiplicand, base))
                break
    if not valid:
        sys.exit(-1)


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
        input_x = str(accumulator).upper()
        input_y = str(multiplicands.pop()).upper()

        log_debug('x: {}'.format(input_x))
        log_debug('y: {}'.format(input_y))
        x = input_x[::-1]  # Reverse string so we can do right-to-left processing left-to-right
        y = input_y[::-1]
        log_debug('x reversed: {}'.format(x))
        log_debug('y reversed: {}'.format(y))


        partial_products = []
        final_products = []
        for y_digit in y:
            log_debug('y_digit: {}'.format(y_digit))
            out_str = ''
            carry_in = 0
            for x_digit in x:
                log_debug('x_digit: {}'.format(x_digit))
                (carry_out, output) = divmod(digits.index(x_digit) * digits.index(y_digit), base)
                log_debug('output without carry_in: {}'.format(output))
                log_debug('carry_out: {}'.format(carry_out))
                output += carry_in
                log_debug('output with carry_in: {}'.format(output))
                while output >= base:
                    (extra_carry_out, output) = divmod(output, base)
                    log_debug('extra carry_out: {}'.format(extra_carry_out))
                    carry_out += extra_carry_out
                    log_debug('new total carry_out: {}'.format(carry_out))

                assert(output < base)
                out_str = '{}{}'.format(digits[output], out_str)
                log_debug('out_str: {}'.format(out_str))
                carry_in = carry_out
            if carry_out:
                out_str = '{}{}'.format(digits[carry_out], out_str)
                log_debug('output after applying leftover carry_out ({}): {}'.format(digits[carry_out], out_str))
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
