#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import hashlib
import sys

from socket import gethostname


###############################################################################
# Constants                                                                   #
###############################################################################

# prompt length limits
MAX_PROMPT_LENGTH = 38
MAX_REPO_LENGTH = 11
REPO_NAME_FRACTION = 0.75
MAX_BRANCH_LENGTH = 11
BRANCH_FRACTION = 0.75

# user specific info
MY_USERNAME = "brian"
if len(sys.argv) > 1:
    MY_HOSTNAME = sys.argv[1]
else:
    MY_HOSTNAME = "muffin"

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

vcs_subdirs = [".svn", ".git"]


###############################################################################
# Helper functions                                                            #
###############################################################################

def repo_information(pwd):
    pwd_list = pwd.split("/")
    current_dir = ["/"]

    distance_from_root = 1

    last_with_vcs = "."
    while distance_from_root <= len(pwd_list):
        if has_vcs_subdir(current_dir):
            last_with_vcs = current_dir
        distance_from_root += 1
        current_dir = pwd_list[:distance_from_root]

    repo_path = ""
    repo_name = ""
    vcs_subdir = get_vcs_subdir(last_with_vcs)
    if vcs_subdir:
        repo_path = "/".join(last_with_vcs)
        repo_name = os.path.basename(repo_path)

    return repo_name, repo_path, vcs_subdir


def has_vcs_subdir(current_dir):
    return get_vcs_subdir(current_dir)


def get_vcs_subdir(current_dir):
    for vcs_subdir in vcs_subdirs:
        candidate = vcs_candidate_dir(current_dir, vcs_subdir)
        if os.path.exists(candidate):
            return vcs_subdir
    return ""


def vcs_candidate_dir(current_dir, vcs_subdir):
    dir_string = "/".join(current_dir)
    vcs_candidate = os.path.join(dir_string, vcs_subdir)
    return vcs_candidate


def get_branch_name(repo_path, vcs_subdir):
    try:
        vcs_obj = os.path.join(repo_path, vcs_subdir)

        if os.path.isdir(vcs_obj):
            head_filepath = os.path.join(vcs_obj, "HEAD")
            with open(head_filepath) as head_file:
                ref_line = head_file.readline().strip()
                branch_name = ref_line.split("/")[-1]
                return branch_name
        elif os.path.isfile(vcs_obj):
            return "SUBMODULE"
        else:
            return ""
    except FileNotFoundError:
        return ""


def format_repo_name(repo_name):
    return format_name(repo_name, "{}[{}]{}")


def format_branch_name(branch_name):
    return format_name(branch_name, "{}({}){}")


def format_name(name, format_string):
    if name:
        color = name_color(name)
        formatted = format_string.format(color, name, RS)
    else:
        formatted = ""

    return formatted


def name_color(name):
    encoded_name = name.encode('utf-8')
    color_digest = hashlib.sha256(encoded_name).hexdigest()
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

    repo, repo_path, vcs_subdir = repo_information(pwd)
    repo = limit_path_length(repo, MAX_REPO_LENGTH, REPO_NAME_FRACTION)

    branch = get_branch_name(repo_path, vcs_subdir) if repo else ""
    branch = limit_path_length(branch, MAX_BRANCH_LENGTH, BRANCH_FRACTION)

    # need to get length of repo string before adding color chars
    unformatted_repo_length = len(repo) + 2 if repo else 0
    unformatted_branch_length = len(branch) + 2 if branch else 0
    pwd_length = MAX_PROMPT_LENGTH - unformatted_repo_length - unformatted_branch_length

    repo = format_repo_name(repo)
    branch = format_branch_name(branch)

    homedir = os.path.expanduser('~')
    pwd = pwd.replace(homedir, '~', 1)

    if repo:
        pwd = limit_path_length(pwd, pwd_length, 1.0)
    else:
        pwd = limit_path_length(pwd, pwd_length, 0.75)

    if username != MY_USERNAME or hostname != MY_HOSTNAME:
        prompt = '{0}@{1}:{2}{3}'.format(username, hostname, pwd, CURSOR)
    else:
        prompt = ''.join([repo, FGRN, pwd, RS, branch, FYEL, CURSOR, RS])

    print(prompt)


if __name__ == '__main__':
    main()
