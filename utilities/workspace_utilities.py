from i3ipc.aio import Connection
import asyncio, time, itertools

import utilities.container_utilities as con_utils
import utilities.application_utilities as app_utils

"""
Returns a Con object for the workspace with
a name matching the name passed.

Returns None if no corresponding workspace
can be found.
"""
async def get_workspace(name, connection):
    workspace = None
    tree = await connection.get_tree()

    #This "drills down" through the tree to get the
    #actual Con objects for the workspaces
    workspaces = tree.nodes[1].nodes[1].nodes

    for node in workspaces:
        if node.name == name:
            workspace = node

    return workspace


"""
Returns a Con object of the currently-focused
workspace
"""
async def get_focused_workspace(connection):
    workspace = None
    tree = await connection.get_tree()

    workspaces = tree.nodes[1].nodes[1].nodes

    for node in workspaces:
        focused = await con_utils.get_focused_container(node)

        if focused:
            workspace = node

    return workspace


"""
Checks if the workspace Con object passed is
empty
"""
def is_empty(workspace):
    return len(workspace.nodes) > 0

"""
Checks if the workspace is setup according
to the Desktop manager
"""
def is_setup(workspace):
    setup = False

    if len(workspace.nodes) == 3 and workspace.layout == "splith":
        setup = True

        left = workspace.nodes[0]
        middle = workspace.nodes[1]
        right = workspace.nodes[2]

        if len(left.nodes) == 2 and left.layout == "splitv":
            setup = setup and True
        else:
            setup = False

        #Either the middle pane has only one application
        #in which case it has zero children; or it has
        #multiple applications, in which case it has
        #non-zero children
        if len(middle.nodes) == 0:
            #If there is only one application, it should
            #be feh
            setup = setup and (middle.name.find("feh") != -1)
        else:
            #If there are multiple applications
            #it should be tabbed
            pass
            #setup = setup and (middle.layout == "tabbed")

        #Don't really need to check the right column...
        #it's pretty simple for now. Sort of a placeholder.

    return setup

"""

"""
async def handle_setup(workspace, connection=None):
    #workspace = await get_workspace(workspace, connection)
    #await workspace.command("focus")
    tree = await connection.get_tree()
    await tree.command("workspace number " + workspace)

    terminalA = await app_utils.start_application(
        'urxvt -hold -e sh -c "sh /home/iranon/projects/python/desktop-manager/run-fzf.sh"',
        connection=connection
    )
    #await terminalA.command("move to workspace " + str(workspace))

    feh = await app_utils.start_application("feh /home/iranon/pictures/wallpapers/1581731934060.png", connection=connection)
    #await feh.command("move to workspace " + str(workspace))

    terminalB = await app_utils.start_application("urxvt", connection=connection)
    #await terminalB.command("move to workspace " + str(workspace))

    #await terminalA.command("resize set width 20 ppt")
    await feh.command("resize set width 65 ppt")
    await feh.command("tabbed")

    await terminalA.command("split vertical")
    await terminalA.command("focus")
    #result = await terminalA.command("exec sh ~/projects/python/desktop-manager/run-fzf.sh")

    terminalC = await app_utils.start_application(
        "urxvt",
        connection=connection)
    await terminalC.command("resize set height 75 ppt")
