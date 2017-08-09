#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import argparse
import os
import subprocess

from datetime import datetime

###############################################################################
# Constants                                                                   #
###############################################################################

JOURNAL_DIR = os.path.abspath("/home/brian/journal")
EDITOR = os.getenv("EDITOR")


###############################################################################
# Helpers                                                                     #
###############################################################################

def get_day_file(now):
    return os.path.join(get_month_dir(now), now.strftime('%d'))


def get_month_dir(now):
    return os.path.join(get_year_dir(now), now.strftime('%m'))


def get_year_dir(now):
    return os.path.join(JOURNAL_DIR, "years", now.strftime('%Y'))


def edit_file(filename):
    subprocess.call([EDITOR, filename])


def get_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--day",
                       action="store_true",
                       help="open journal entry for the day")
    group.add_argument("-m", "--month",
                       action="store_true",
                       help="open journal directory for current month")
    group.add_argument("-y", "--year",
                       action="store_true",
                       help="open journal directory for current year")
    return parser.parse_args()


###############################################################################
# Main                                                                        #
###############################################################################

def main():

    args = get_args()

    now = datetime.now()

    if args.day:
        month_dir = get_month_dir(now)
        os.makedirs(month_dir, exist_ok=True)
        edit_file(get_day_file(now))
        print("Opening file for {}".format(now.date()))
    elif args.month:
        month_dir = get_month_dir(now)
        os.makedirs(month_dir, exist_ok=True)
        print(month_dir)
    elif args.year:
        year_dir = get_year_dir(now)
        os.makedirs(year_dir, exist_ok=True)
        print(year_dir)


if __name__ == '__main__':
    main()
