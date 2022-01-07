import sys

DEFAULT_LIST = [
    "browse",
    "note",
    "editor",
    "office",
    "chat",
    "passwords"
]

OPTIONS = {
    "browse": ["unjailed"],
    "note": ["wiki","blog", "projects"],
    "office": ["log", "record", "regimen"]
}

SPECIAL = {
    "editor",
    "wiki"
}

def utility(arguments):

    if len(arguments) == 1:
        print_list(DEFAULT_LIST)
    else:
        if arguments[1] in OPTIONS:
            print_list(OPTIONS[arguments[1]])
        else:
            print_list(DEFAULT_LIST)




def print_list(list):
    for item in list:
        print(item)


utility(sys.argv)
