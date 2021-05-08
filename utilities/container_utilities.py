import asyncio, time, itertools

import utilities.workspace_utilities as ws_utils

"""
Returns the currently-focused descendant of a container,
or None, if there is none
"""
async def get_focused_container(container):
    #print("Recursively searching for focused in... " + container.name)
    focused = None

    if len(container.nodes) > 0:
        for node in container.nodes:
            focused = await get_focused_container(node)

    if container.focused == True:
        focused = container

    return focused

"""
Returns the 'main' container of the workspace.
"""
def get_main(workspace):
    main = None

    if ws_utils.is_setup(workspace):
        main = workspace.nodes[1]

    return main

"""
Returns the 'left' column container of the workspace
"""
async def get_left(workspace):
    pass

"""
Returns the 'right' column container of the workspace
"""
async def get_right(workspace):
    pass

"""
Checks if the main container of a workspace
is currently "in use", i.e., has any applications
other than feh running.
"""
def used_main(workspace):
    used = False
    main = get_main(workspace)

    if main:
        used = len(main.nodes) != 0

    return used
