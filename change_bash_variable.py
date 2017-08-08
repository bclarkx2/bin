#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import argparse


###############################################################################
# Constants                                                                   #
###############################################################################

VARIABLES_FILEPATH = os.path.expanduser("~/.bash_variables")


###############################################################################
# Helper functions                                                            #
###############################################################################

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("variable")
    parser.add_argument("new_value")
    return parser.parse_args()


def build_new_var_lines(old_var_lines, variable, new_value):
    new_var_lines = []
    for line in old_var_lines:
        if contains_var(line, variable):
            new_var_lines.append(var_line(variable, new_value))
        else:
            new_var_lines.append(line)
    return new_var_lines


def contains_var(line, variable):
    export_string = "export {}=".format(variable)
    return export_string in line


def var_line(variable, new_value):
    return "export {}=\"{}\"\n".format(variable, new_value)


###############################################################################
# Main script                                                                 #
###############################################################################

def main():
    args = get_args()

    with open(VARIABLES_FILEPATH, 'r') as variables_file:
        old_var_lines = variables_file.readlines()

    new_var_lines = build_new_var_lines(old_var_lines, args.variable, args.new_value)

    with open(VARIABLES_FILEPATH, 'w') as variables_file:
        variables_file.write("".join(new_var_lines))


if __name__ == '__main__':
    main()
