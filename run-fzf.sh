#read path <<< $(echo $HOME"/projects/python/desktop-manager")
manager_path="/opt/desktop-manager"

read arg <<< $(
  python3 $manager_path/fzf-manager/list-helper.py |
  fzf --bind 'tab:reload(python3 /opt/desktop-manager/fzf-manager/list-helper.py {})' \
    --layout=reverse
  )

python3 $manager_path/fzf_helper.py $arg
sh $manager_path/run-fzf.sh

#
# --header=STR
#
#
