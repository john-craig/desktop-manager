from i3ipc.aio import Connection
import asyncio, time, itertools

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

#Event handling

def on_event(conn, data):
    conn.main_quit()

    return data

#Window utility

async def start_application(name, connection=None):
    if not connection:
        return

    global reply
    reply = None

    #start_event = lambda conn, data: callback(conn, data)
    def callback(conn, data):
        global reply
        reply = data

        conn.main_quit()

    connection.on(
        'window::new',
        callback
    )

    await connection.command("exec " + name)

    await connection.main()
    connection.off(callback)

    return reply.container


#Main functions

async def run_setup(workspace=1, connection=None):

    terminalA = await start_application(
        'urxvt -hold -e sh -c "sh /home/iranon/projects/python/desktop-manager/run-fzf.sh"',
        connection=connection
    )
    await terminalA.command("move to workspace " + str(workspace))

    feh = await start_application("feh /home/iranon/pictures/wallpapers/1581731934060.png", connection=connection)
    await feh.command("move to workspace " + str(workspace))

    terminalB = await start_application("urxvt", connection=connection)
    await terminalB.command("move to workspace " + str(workspace))

    #await terminalA.command("resize set width 20 ppt")
    await feh.command("resize set width 65 ppt")
    await feh.command("tabbed")

    await terminalA.command("split vertical")
    await terminalA.command("focus")
    #result = await terminalA.command("exec sh ~/projects/python/desktop-manager/run-fzf.sh")

    terminalC = await start_application(
        "urxvt",
        connection=connection)
    await terminalC.command("resize set height 75 ppt")

async def switch_to(workspace, connection=None):
    #First check if the target workspace is set up
    #yet. If it is not,
    pass

async def main_application(command, connection=None):
    if not connection:
        raise Error("Something starting a primary application")

    tree = await connection.get_tree()
    workspace_num = get_current_workspace(tree)

    workspace_container = get_workspace_container(tree, workspace_num)

    print(workspace_container)



#Driver

async def manager(args):
    windows = (
     '1', '2', '3', '4', '5', '6', '7', '8', '9'
    )
    i3 = await Connection().connect()

    print(args)

    if len(args) == 1:
        await run_setup(connection=i3)
    #If it is a workspace number, assume we are switching
    #over to it
    elif args[1] in windows:
        await switch_to(int(args[1]), connection=i3)
    #Otherwise it is a command to open in main
    #display
    else:
        await main_application(args[1], connection=i3)

def drive(args):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(manager(args))
    finally:
        loop.close()
        print("FAS")

#
#
# drive(sys.args)

# i3.on('window::new', on_new_window)
#
# # i3.main()
# def default_workspace():
#     #Start Urxvt
#     i3.command("exec -name leftColumnTerminal i3-sensible-terminal")
#
#     i3.command("exec feh /home/iranon/sync/pictures/wallpapers/1581731934060.png")
#
#     i3.command("exec i3-sensible-terminal")
#     #
#     # i3.command("focus prev; focus prev;")
#     #
#     # i3.command("resize set width 20 ppt")
#     #
#     # i3.command("focus next; focus next;")
#     #
#     # i3.command("resize set width 20 ppt")
#
#
# default_workspace()
