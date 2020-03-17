#!/usr/bin/env bash

arg="$1"

if [[ -z "$arg" ]] ; then
	echo "Missing argument: must supply a git command"
fi

case $arg in
	"s")
		command="status"
		shift
		;;
	
	"d")
		command="diff"
		shift
		;;

	"a")
		command="add"
		shift
		;;

	"aa")
		command="add ."
		shift
		;;

	"c")
		command="commit"
		shift
		;;

	"cm")
		command="commit -m"
		shift
		;;
	
	"f")
		command="fetch"
		shift
		;;	
esac

if [[ ! -z ${command+x} ]] ; then
	echo git $command "$@"
	git $command "$@"
else
	echo git "$@"
	git "$@"
fi
