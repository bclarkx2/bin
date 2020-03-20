# About

Common tools for a Linux environment that is similar to bash + Ubuntu.

Includes scripts for working with these notable items, among others:
- bash
- vim
- grive

# Installation

Clone this repo to a preferred location for scripts (e.g. `$HOME/bin` for a user-specific install, or `/usr/bin` for a system-wide install)

`git clone git@github.com:bclark/bin ~`

Then, ensure that the install directory is included on your PATH. Add the following line to your shell init script (e.g. `.bashrc` for bash). Or, checkout [dotfiles](https://github.com/bclarkx2/dotfiles) for a different way to set up your shell init scripts!

`export PATH="$PATH:$HOME/bin"`

Then, refresh your shell to be able to call scripts from this repo from anywhere. See the `refresh-bash` script for a tool to easily reload your shell configs!

# Usage

- Add a new script to this directory with `newscript`. 
- Make all files in `bin` executable using `permit-bin`

# Notes

- Some of these scripts are marked as bash scripts even though they are certainly POSIX compliant. :shrug:

