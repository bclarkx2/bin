#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import hashlib

from socket import gethostname


###############################################################################
# Constants                                                                   #
###############################################################################

# prompt length limits
MAX_PROMPT_LENGTH = 35
MAX_REPO_LENGTH = 11
REPO_NAME_FRACTION = 0.75

# user specific info
MY_USERNAME = "brian"
MY_HOSTNAME = "bclark-ubuntu"

# prompt text constants
CURSOR = '$ '
ELLIPSIS = ".."

# colors
RS = "\[\033[0m\]"     # reset
HC = "\[\033[1m\]"     # hicolor
UL = "\[\033[4m\]"     # underline
INV = "\[\033[7m\]"    # inverse background and foreground
FBLK = "\[\033[30m\]"  # foreground black
FRED = "\[\033[31m\]"  # foreground red
FGRN = "\[\033[32m\]"  # foreground green
FYEL = "\[\033[33m\]"  # foreground yellow
FBLE = "\[\033[34m\]"  # foreground blue
FMAG = "\[\033[35m\]"  # foreground magenta
FCYN = "\[\033[36m\]"  # foreground cyan
FWHT = "\[\033[37m\]"  # foreground white
BBLK = "\[\033[40m\]"  # background black
BRED = "\[\033[41m\]"  # background red
BGRN = "\[\033[42m\]"  # background green
BYEL = "\[\033[43m\]"  # background yellow
BBLE = "\[\033[44m\]"  # background blue
BMAG = "\[\033[45m\]"  # background magenta
BCYN = "\[\033[46m\]"  # background cyan
BWHT = "\[\033[47m\]"  # background white

colors = [FRED, FYEL, FBLE, FMAG, FCYN, FWHT]


###############################################################################
# Helper functions                                                            #
###############################################################################

def get_svn_repo_name_from_tail(pwd):

    current_dir = pwd.split("/")

    while current_dir and not has_svn_subdir(current_dir):
        current_dir = current_dir[:-1]

    repo_name = ""
    if current_dir:
        repo_path = "/".join(current_dir)
        repo_name = os.path.basename(repo_path)

    return repo_name


def get_svn_repo_name_from_head(pwd):

    pwd_list = pwd.split("/")
    current_dir = ["/"]

    distance_from_root = 1

    while distance_from_root <= len(pwd_list) and not has_svn_subdir(current_dir):
        distance_from_root += 1
        current_dir = pwd_list[:distance_from_root]

    repo_name = ""
    if has_svn_subdir(current_dir):
        repo_path = "/".join(current_dir)
        repo_name = os.path.basename(repo_path)

    return repo_name


def has_svn_subdir(current_dir):
    return os.path.isdir(svn_candidate_dir(current_dir))


def svn_candidate_dir(current_dir):
    dir_string = "/".join(current_dir)
    svn_candidate = os.path.join(dir_string, ".svn")
    return svn_candidate


def format_repo_name(repo_name):
    if repo_name:
        color = repo_color(repo_name)
        formatted = "{}[{}]{}".format(color, repo_name, RS)
    else:
        formatted = ""

    return formatted


def repo_color(repo_name):
    encoded_repo_name = repo_name.encode('utf-8')
    color_digest = hashlib.sha256(encoded_repo_name).hexdigest()
    color_index = int(color_digest, 16) % len(colors)
    return colors[color_index]


def limit_path_length(path, path_length, second_half_fraction):

    formatted = path

    if len(path) > path_length:

        usable_length = path_length - len(ELLIPSIS)

        first_half_fraction = 1 - second_half_fraction
        second_half_fraction = second_half_fraction

        first_part_length = rnd(usable_length * first_half_fraction)
        second_part_length = rnd(usable_length * second_half_fraction)

        first_part = path[:first_part_length]
        second_part = path[-1 * second_part_length:]

        formatted = ''.join([first_part, ELLIPSIS, second_part])

    return formatted


def rnd(arg):
    return int(round(arg))


###############################################################################
# Main                                                                        #
###############################################################################

def main():

    hostname = gethostname()
    username = os.environ['USER']

    try:
        pwd = os.getcwd()
    except OSError:
        pwd = "DNE"

    repo = get_svn_repo_name_from_head(pwd)
    repo = limit_path_length(repo, MAX_REPO_LENGTH, REPO_NAME_FRACTION)

    # need to get length of repo string before adding color chars
    unformatted_repo_length = len(repo) + 2 if repo else 0
    pwd_length = MAX_PROMPT_LENGTH - unformatted_repo_length

    repo = format_repo_name(repo)

    homedir = os.path.expanduser('~')
    pwd = pwd.replace(homedir, '~', 1)

    if repo:
        pwd = limit_path_length(pwd, pwd_length, 1.0)
    else:
        pwd = limit_path_length(pwd, pwd_length, 0.75)

    if username != MY_USERNAME or hostname != MY_HOSTNAME:
        prompt = '{0}@{1}:{2}{3}'.format(username, hostname, pwd, CURSOR)
    else:
        prompt = ''.join([repo, FGRN, pwd, RS, FYEL, CURSOR, RS])

    print(prompt)


if __name__ == '__main__':
    main()
