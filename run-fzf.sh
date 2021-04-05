#!/bin/bash
read arg <<< $(echo -e 'A\nFew\nChoices' | fzf -- layout=reverse)
python3 ./fzf-helper.py $arg
#sh run-fzf.sh
