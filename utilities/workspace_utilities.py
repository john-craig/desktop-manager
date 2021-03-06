from i3ipc.aio import Connection
import asyncio, time, itertools
import subprocess

import utilities.container_utilities as con_utils
import utilities.application_utilities as app_utils


async def get_workspaces(connection):
    tree = await connection.get_tree()

    #This "drills down" through the tree to get the
    #actual Con objects for the workspaces
    workspaces = tree.nodes[1].nodes[1].nodes

    return workspaces

"""
Returns a Con object for the workspace with
a name matching the name passed.

Returns None if no corresponding workspace
can be found.
"""
async def get_workspace(name, connection):
    workspace = None
    workspaces = await get_workspaces(connection)

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
        focused = node.find_focused()

        if focused:
            workspace = node

    return workspace

"""
Sets the currently-focused workspace to the
workspace passed.
"""
async def set_focused_workspace(name, connection):
    tree = await connection.get_tree()
    await tree.command("workspace number " + name)

"""
Returns the name of the next available workspace
"""
async def next_available_workspace(connection):
    workspace_names = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
    workspaces = await get_workspaces(connection)
    next = None

    name_idx = 0
    ws_idx = 0

    while name_idx < len(workspace_names) and ws_idx < len(workspaces) and not next:
        if workspace_names[name_idx] != workspaces[ws_idx].name:
            next = workspace_names[name_idx]

        name_idx +=1
        ws_idx +=1

    if not next and ws_idx == len(workspaces):
        if name_idx < len(workspace_names):
            next = workspace_names[name_idx]

    return next


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
            #setup = setup and (middle.name.find("i3-msg") != -1)
            setup = setup and True
        else:
            #If there are multiple applications
            #it should be tabbed
            pass
            #setup = setup and (middle.layout == "tabbed")

        #Don't really need to check the right column...
        #it's pretty simple for now. Sort of a placeholder.

    return setup

"""
Checks if the current workspace contains the
same application as the one passed
"""
def same_application(workspace, application):
    same = False
    main = con_utils.get_main(workspace)

    if main and len(main.nodes) > 0:
        for con in main.nodes:
            if 'window_properties' in con.ipc_data:
                application_name = application.lower().split(" ")[0]
                class_name = con.ipc_data['window_properties']['class'].lower()

                if class_name == application_name:
                    same = True
    
    return same

"""

"""
async def handle_setup(workspace, connection=None):
    #workspace = await get_workspace(workspace, connection)
    #await workspace.command("focus")
    await set_focused_workspace(workspace, connection)

    terminalA = await app_utils.start_application(
        #'alacritty --hold --command sh /opt/desktop-manager/run-fzf.sh',
        'wezterm start -- bash -c /opt/desktop-manager/run-fzf.sh',
        connection=connection
    )
    #await terminalA.command("move to workspace " + str(workspace))
    await terminalA.command('mark control-panel-' + str(workspace))

    feh = await app_utils.start_application("feh /home/iranon/.config/images/spacer.png", connection=connection)
    #await feh.command("move to workspace " + str(workspace))

    #terminalB = await app_utils.start_application("alacritty", connection=connection)
    terminalB = await app_utils.start_application("wezterm", connection=connection)
    await terminalB.command("mark left-panel")
    #await terminalB.command("move to workspace " + str(workspace))

    #await terminalA.command("resize set width 20 ppt")
    await feh.command("resize set width 65 ppt")
    await feh.command("tabbed")

    await terminalA.command("split vertical")
    await terminalA.command("focus")
    #result = await terminalA.command("exec sh ~/projects/python/desktop-manager/run-fzf.sh")

    terminalC = await app_utils.start_application(
        #"alacritty",
        "wezterm",
        connection=connection)
    await terminalC.command("resize set height 75 ppt")
    await terminalC.command("mark right-panel")

    await terminalA.command("focus")


"""
Searched all setup workspaces and returns one that has
a matching application running in it, if there is one
"""
async def find_next_matching_workspace(application, connection):
    workspaces = await get_workspaces(connection)
    match = None

    for ws in workspaces:
        if is_setup(ws):
            if same_application(ws, application):
                match = ws


    return match