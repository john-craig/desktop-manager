from i3ipc.aio import Connection
import asyncio, time, itertools

import utilities.workspace_utilities as ws_utils
import utilities.application_utilities as app_utils

#Tree parsing

def get_workspace_container(tree, index):
    hdmi = tree.ipc_data['nodes'][1]
    content = hdmi['nodes'][1]

    return content['nodes'][index]

def get_current_workspace(tree):
    focused = tree.find_focused()
    id = focused.workspace().ipc_data['id']
    num = -1

    workspaces = tree.ipc_data['nodes'][1]['nodes'][1]['nodes']

    for i in range(0, len(workspaces)):
        if workspaces[i]['id'] == id:
            num = i + 1

    return num


#Main functions


async def switch_to(workspace, connection=None):
    #First check if the target workspace is set up
    #yet. If it is not,
    pass

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


    if ws_utils.is_setup(workspace):
        used = con_utils.used_main(workspace)

        if used:
            pass
            # # TODO: change to next available workspace

        main = con_utils.get_main(workspace)

        await main.command("focus")
        await main.command("split vertical")
        await main.command("exec " + application)
        await main.command("layout tabbed")
    else:
        pass
        ## TODO: Create setup method



#Driver

async def manager(args):
    windows = (
     '1', '2', '3', '4', '5', '6', '7', '8', '9'
    )
    i3 = await Connection().connect()

    #print(args)

    if len(args) == 1:
        await ws_utils.handle_setup(windows[0], connection=i3)
    #If it is a workspace number, assume we are switching
    #over to it
    #elif args[1] in windows:
        #await switch_to(int(args[1]), connection=i3)
    #Otherwise it is a command to open in main
    #display
    else:
        #await main_application(args[1], connection=i3)
        workspace_1 = await ws_utils.get_workspace('1', i3)

        await start_main_application(
            "firejail chromium",
            i3,
            workspace=workspace_1
        )



def drive(args):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(manager(args))
    finally:
        loop.close()
