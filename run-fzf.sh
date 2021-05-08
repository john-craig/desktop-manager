#!/bin/bash
read arg <<< $(cat $HOME/projects/python/desktop-manager/options.txt | fzf --layout=reverse)
python3 $HOME/projects/python/desktop-manager/fzf_helper.py $arg
sh $HOME/projects/python/desktop-manager/run-fzf.sh
