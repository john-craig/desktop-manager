import sys

DEFAULT_LIST = [
    "browse", "note", "editor", "office"
]

OPTIONS = {
    "browse": ["unjailed"],
    "editor": ["blog"],
    "office": ["log", "record", "regimen"]
}

def utility(arguments):

    if len(arguments) == 1:
        print_list(DEFAULT_LIST)
    else:
        if arguments[1] in OPTIONS:
            print_list(OPTIONS[arguments[1]])




def print_list(list):
    for item in list:
        print(item)


utility(sys.argv)
