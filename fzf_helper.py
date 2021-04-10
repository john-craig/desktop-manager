import i3_helper as i3_helper
import sys, subprocess

def utility(arguments):
    options = {
        'browse': "firejail chromium"
    }

    if len(arguments) == 1:
        i3_helper.drive(arguments)

utility(sys.argv)
