#! /usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import argparse
import subprocess

###############################################################################
# Constants                                                                   #
###############################################################################

LIBS = ["xrepl", "racket/trace"]


###############################################################################
# Helper functions                                                            #
###############################################################################

def option_list(option, lis):
    res = []
    for value in lis:
        res.extend([option, value])
    return res


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files",
                        nargs="*")
    return parser.parse_args()


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    args = get_args()

    arg_lst = ["racket"]
    arg_lst += option_list("-f", args.files)
    arg_lst += option_list("-l", LIBS)
    arg_lst += ["-i"]

    subprocess.call(arg_lst)


if __name__ == '__main__':
    main()
