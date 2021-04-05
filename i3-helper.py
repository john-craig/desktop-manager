from i3ipc.aio import Connection
import asyncio, time, itertools

# Create the Connection object that can be used to send commands and subscribe
# to events.
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


def on_event(conn, data):
    conn.main_quit()

    return data


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

    return reply.container

async def set_application_property(property, app_id, connection):
    reply = await connection.command("[id=\"" + str(app_id) + "\"] " + property)
    print(reply[0].ipc_data)


async def run_setup(workspace=1, connection=None):

    terminalA = await start_application("urxvt", connection=connection)
    await terminalA.command("move to workspace " + str(workspace))

    feh = await start_application("feh /home/iranon/sync/pictures/wallpapers/1581731934060.png", connection=connection)
    await feh.command("move to workspace " + str(workspace))

    terminalB = await start_application("urxvt", connection=connection)
    await terminalB.command("move to workspace " + str(workspace))

    #await terminalA.command("resize set width 20 ppt")
    await feh.command("resize set width 65 ppt")

    await terminalA.command("split vertical")
    await terminalA.command("focus")
    #result = await terminalA.command("exec sh ~/projects/python/desktop-manager/run-fzf.sh")

    terminalC = await start_application(
        'urxvt -hold -e sh -c "sh /home/iranon/projects/python/desktop-manager/run-fzf.sh"',
        connection=connection)
    await terminalC.command("move to workspace " + str(workspace))
    await terminalC.command("move left")
    await terminalC.command("move up")





async def manager():
    i3 = await Connection().connect()

    await run_setup(connection=i3)

def drive():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(manager())
    finally:
        loop.close()




drive()

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
