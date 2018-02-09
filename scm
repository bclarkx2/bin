#! /usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import argparse
import subprocess


###############################################################################
# Helper functions                                                            #
###############################################################################

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

    file_lst = []

    for f in args.files:
        file_lst.extend(["-f", f])

    arg_lst = ["racket"] + file_lst + ["-i"]

    subprocess.call(arg_lst)


if __name__ == '__main__':
    main()
