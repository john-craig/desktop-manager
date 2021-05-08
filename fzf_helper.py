import i3_helper as i3_helper
import sys, subprocess

def utility(arguments):
    options = {
        'browse': "firejail chromium",
        'atom': "atom"
    }

    if len(arguments) == 2:
        if arguments[1] in options:
            arguments[1] = options[arguments[1]]
            
            i3_helper.drive(arguments)

utility(sys.argv)
