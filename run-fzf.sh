#!/bin/bash
read path <<< $(echo $HOME"/projects/python/desktop-manager")
#read path <<< $(realpath .)
echo $path

read arg <<< $(
  python3 $path/fzf-manager/list-helper.py |
  fzf --bind 'tab:reload(python3 fzf-manager/list-helper.py {})' \
    --layout=reverse
  )

python3 $path/fzf_helper.py $arg
sh $path/run-fzf.sh

#
# --header=STR
#
#
