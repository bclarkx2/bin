#!/usr/bin/env python3

"""Utility to open both .cpp and .h files together

Give the filename as the first positional argument. Periods at the end will be stripped. Must have $EDITOR environment variable defined.
"""

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import argparse
import subprocess

###############################################################################
# Constants                                                                   #
###############################################################################

EXTENSIONS = [".h", ".cpp"]


###############################################################################
# Helper functions                                                            #
###############################################################################

def get_args():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="file to open")
    return parser.parse_args()


def open_all(editor, filename, extensions):

    for extension in extensions:
        subprocess.call([editor, filename + extension])


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    args = get_args()

    editor = os.getenv("EDITOR", "vi")

    filename = args.filename.rstrip(".")

    open_all(editor, filename, EXTENSIONS)


if __name__ == '__main__':
    main()
