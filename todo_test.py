#!/usr/bin/env python3
"""Utility to view unwritten tests

Defines a comment format to allow you to write some
basic details about a unit test that you are not
going to write at the moment, but that you or somebody
should think about coming back and writing at some
point in time. Format:

# @TODO
# <tag>: <value>
# <tag>: <value>
...
# @END

You can use any number of tags, followed by any
string value. Current tags:

{unit, test, description, priority}

This script will generate a report on stdout
giving all the tagged information about the test,
as well as the file and line number to find it.
"""

###############################################################################
# Imports                                                                     #
###############################################################################

import glob
import json
import argparse
import sys

###############################################################################
# Constants                                                                   #
###############################################################################

KEYWORDS = ["unit", "test", "priority", "description"]


###############################################################################
# Helper functions                                                            #
###############################################################################

def get_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f",
                        "--file",
                        action='append',
                        help="Get TODO tests from one file")
    parser.add_argument("-a",
                        "--all",
                        action="store_true",
                        help="See output from all files")
    parser.add_argument("-s",
                        "--save",
                        default=sys.stdout,
                        const="todo_report",
                        nargs="?",
                        help="save report to a file")
    return parser.parse_args()


def set_files(args):

    if args.file:
        files = args.file
    else:
        files = glob.glob("test_*.py")
    return files


def report_from_files(files):
    tests = {}
    for file in files:
        tests[file] = todo_blocks_from_file(file)
    return tests


def todo_blocks_from_file(filepath):

    lines = extract_lines_from_file(filepath)
    todo_blocks = todo_blocks_from_lines(lines, filepath)
    return todo_blocks


def extract_lines_from_file(filepath):
    with open(filepath, 'r') as the_file:
        lines = the_file.readlines()
        if lines[len(lines) - 1] != "\n":
            lines.append("\n")  # extra line at the end to prevent index error

    return lines


def todo_blocks_from_lines(lines, filepath):

    todo_blocks = []

    start_index = -1
    end_index = -1

    for idx, line in enumerate(lines):

        if has_comment_tag(line, "TODO"):
            start_index = idx

        elif has_comment_tag(line, "END"):

            # do this check to prevent misplaced tags from adding fake entries
            if start_index > end_index:
                end_index = idx
                comment_block = lines[start_index:end_index + 1]
                todo_blocks.append({
                    "info": comment_to_todo_block(comment_block),
                    "line": filepath + ":" + str(start_index + 1),
                })

    return todo_blocks


def has_comment_tag(line, tag):
    return line.strip().replace("# @", "") == tag


def comment_to_todo_block(comment_block):

    comment_block.pop(0)
    comment_block.pop()

    comment_block = [line.replace("#", "").strip() for line in comment_block]

    todo_block = {}
    for line in comment_block:
        split = line.split(":")
        keyword_candidate = split[0].strip()
        remainder = split[1].strip()

        if len(split) == 2 and keyword_candidate in KEYWORDS:
            todo_block[keyword_candidate] = remainder

    return todo_block


def write_output(tests, output):

    if output == sys.stdout:
        json.dump(tests, output, sort_keys=True, indent=3)
    else:
        with open(output, 'w') as output_file:
            json.dump(tests, output_file, sort_keys=True, indent=3)
        print("Saving to " + str(output))


###############################################################################
# Main script                                                                 #
###############################################################################

def main():

    args = get_args()

    files = set_files(args)

    tests = report_from_files(files)

    # strip files with no todo tests
    if not args.all:
        tests = {test: tests[test] for test in tests if tests[test]}

    write_output(tests, args.save)


if __name__ == '__main__':
    main()
