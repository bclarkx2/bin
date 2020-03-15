#!/usr/bin/env python3

###############################################################################
# Imports                                                                     #
###############################################################################

import os
import hashlib
import sys

from socket import gethostname
from os import path 
from git import Repo

import subprocess


###############################################################################
# Constants                                                                   #
###############################################################################

# user specific info
MY_USERNAME = os.getenv("MY_USERNAME")
MY_HOSTNAME = os.getenv("MY_HOSTNAME")

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

# Retrieval functions

def repo_information(pwd):
    pwd_list = pwd.split("/")

    repos = []
    last_repo = []
    last_vcs_subdir = ""

    for i in range(2, len(pwd_list)+1):
        current_dir = pwd_list[:i]
        vcs_subdir = get_vcs_subdir(current_dir)
        if vcs_subdir:
            last_repo = current_dir
            repos.append(current_dir[-1])
            last_vcs_subdir = vcs_subdir

    repo_str = "->".join(repos)
    repo_path = "/".join(last_repo)

    return repo_str, repo_path, last_vcs_subdir


def get_vcs_subdir(current_dir):
    for vcs_subdir in vcs_subdirs:
        candidate = "/".join([*current_dir, vcs_subdir])
        if path.exists(candidate):
            return vcs_subdir
    return ""


def branch_name(repo_path, vcs_subdir):
    vcs_obj = path.join(repo_path, vcs_subdir)

    if vcs_subdir == ".git":
        return git_branch_name(repo_path, vcs_subdir)   
    else:
        return "SVN"


def git_branch_name(repo_path, vcs_subdir):
    repo = Repo(repo_path)
    cmd_output = subprocess.run(["git", "status", "-s"], stdout=subprocess.PIPE)

    if len(cmd_output.stdout) > 0:
        fmt = f"{repo.active_branch.name}*"
    else:
        fmt = f"{repo.active_branch.name}"

    return fmt.format()


def virtual_env(pwd):

    # might be in an activated venv
    if sys.prefix != sys.base_prefix:
        venv_name = os.path.basename(sys.prefix)
        return format_name(venv_name, "{}|{}|{}")

    # might be in a directory that contains a venv
    else:

        pwd = os.path.expanduser(pwd)
        _, subdirs, _ = next(os.walk(pwd))

        for subdir in subdirs:
            f = os.path.join(subdir, "bin", "activate")
            if os.path.isfile(f):
                return format_name("ENV", "{}!!{}!!{}")

        return ""


# Format functions

def format_identity(username, hostname):
    if username != MY_USERNAME or hostname != MY_HOSTNAME:
        return f"{username}@{hostname}:"
    else:
        return ""


def format_pwd(pwd):
    homedir = os.path.expanduser('~')
    return pwd.replace(homedir, '~', 1)


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


###############################################################################
# Main                                                                        #
###############################################################################

def main():

    # Extract data
    try:
        pwd = os.getcwd()
    except OSError:
        pwd = "DNE"

    hostname = gethostname()
    username = os.getenv('USER')
    repo, repo_path, vcs_subdir = repo_information(pwd)
    branch = branch_name(repo_path, vcs_subdir) if repo else ""
    virtualenv = virtual_env(pwd)

    # Format pieces for display
    identity = format_identity(username, hostname)
    pwd = format_pwd(pwd)
    repo = format_repo_name(repo)
    branch = format_branch_name(branch)
    
    # Combine into display
    prompt = ''.join([os.linesep, identity, repo, FGRN, pwd, RS, branch, virtualenv, os.linesep, FYEL, CURSOR, RS])
    print(prompt)


if __name__ == '__main__':
    main()
