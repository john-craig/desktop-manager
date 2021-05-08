from i3ipc.aio import Connection
import asyncio, time, itertools

import utilities.workspace_utilities as ws_utils
import utilities.container_utilities as con_utils
import utilities.application_utilities as app_utils


windows = (
 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
)

#Main functions

"""
Switches to the workspace which is passed.
If the workspace is not set up yet, then
it sets it up.
"""
async def switch_to(name, connection=None):
    workspace = await ws_utils.get_workspace(name)

    if not workspace:
        await ws_utils.handle_setup(name, connect)
    else:
        await ws_utils.set_focused_workspace(workspace, connection)

"""
Runs the application as 'exec application'
and starts it in the workspace matching
the passed string.

If no workspace is passed, it attempts to start
it in the current workspace. If the current workspace
is occupied, it starts it in the next available workspace.

If the workspace passed has not yet been populated, it
populates it and starts it there.
"""
async def start_main_application(application, connection, workspace=None, allow_occupied=False):
    #If no workspace specified, get the current workspace
    if not workspace:
        workspace = await ws_utils.get_focused_workspace(connection)

    #Check if the workspace is set-up
    if ws_utils.is_setup(workspace):
        used = con_utils.used_main(workspace)

        #If it is setup but main is in use, setup the next available one
        if used:
            next_avilable = await ws_utils.next_available_workspace(connection)
            await ws_utils.handle_setup(next_avilable, connection)
            workspace = await ws_utils.get_focused_workspace(connection)
    #If it is not set up but it is not empty, set up the next available one
    else:
        next_avilable = await ws_utils.next_available_workspace(connection)
        await ws_utils.handle_setup(next_avilable, connection)
        workspace = await ws_utils.get_focused_workspace(connection)

    #Open the new application in the workspace
    main = con_utils.get_main(workspace)

    await main.command("focus")
    await main.command("split vertical")
    await main.command("exec " + application)
    await main.command("layout tabbed")


#Driver

async def manager(args):
    i3 = await Connection().connect()

    # No additional arguments means we are setting up
    # the first workspace
    if len(args) == 1:
        await ws_utils.handle_setup(windows[0], connection=i3)
    # If the additional argument in a window name, then
    # we are switching to it
    elif args[1] in windows:
        await switch_to(args[1], connection=i3)
    # Debug case
    elif args[1] == "test":
        next_available = await ws_utils.next_available_workspace(i3)
        print(next_available)
    #Otherwise assume it is a command we want to use to
    #open an application inside of a workspace
    else:
        #workspace_1 = await ws_utils.get_workspace('1', i3)

        await start_main_application(
            args[1],
            i3
        #    workspace=workspace_1
        )



def drive(args):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(manager(args))
    finally:
        loop.close()
