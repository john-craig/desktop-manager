from i3ipc.aio import Connection
import asyncio, time, itertools

import utilities.container_utilities as con_utils
import utilities.workspace_utilities as ws_utils

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
