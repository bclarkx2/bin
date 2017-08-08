#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import argparse


###############################################################################
# Constants                                                                   #
###############################################################################

DEFAULT_ONX_IP_VARIABLE = "onx1_IP"


###############################################################################
# Main                                                                        #
###############################################################################

def choose_variable(args):
    if args.number:
        return "onx{}_IP".format(args.number)
    elif args.variable:
        return args.variable
    else:
        return DEFAULT_ONX_IP_VARIABLE


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("new_value")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-n", "--number")
    group.add_argument("-v", "--variable")

    return parser.parse_args()


def main():

    args = get_args()

    variable = choose_variable(args)

    print("{} {}".format(variable, args.new_value))


if __name__ == '__main__':
    main()
