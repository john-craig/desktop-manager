import i3_helper as i3_helper
import sys, subprocess

BLOG_PATH = "~/programming/by_language/markdown/blog"
WIKI_PATH = "~/programming/by_language/markdown/wiki"
PROJ_PATH = "~/programming/by_language/markdown/projects"

def utility(arguments):
    options = {
        'browse': "chromium",
        'unjailed': "chromium",
        'note': "typora",
        'wiki': "typora " + WIKI_PATH,
        'blog': "typora " + BLOG_PATH,
        'projects': "typora " + PROJ_PATH,

        'editor': "vscodium",

        'office': "libreoffice",
        'chat': "lightcord",
        'passwords': "keepassxc"
    }

    if len(arguments) == 2:
        if arguments[1] in options:
            arguments[1] = options[arguments[1]]

            i3_helper.drive(arguments)

utility(sys.argv)
