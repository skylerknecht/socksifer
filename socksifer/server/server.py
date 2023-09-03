import asyncio
import ssl

from .events import Events
from aiohttp import web
from socksifer import sio_server
from socksifer.client import command_line_interface
from socksifer.socks import socks_server_manager

import time
class SocketIOServer:
    NAME = 'SocketIO Server'

    def __init__(self):
        pass

    @staticmethod
    async def ping():
        while True:
            await sio_server.sleep(1)
            await sio_server.emit('ping', time.time())

    @staticmethod
    async def send_tasks():
        while True:
            await sio_server.sleep(0.1)
            for socks_server in socks_server_manager.socks_servers.values():
                for socks_client in socks_server.socks_server.socks_clients:
                    while socks_client.socks_tasks:
                        socks_task = socks_client.socks_tasks.pop(0)
                        await sio_server.emit(socks_task.event, socks_task.data, room=socks_server.socks_server.server_id)

    def run(self, arguments):
        # https://stackoverflow.com/questions/51610074/how-to-run-an-aiohttp-server-in-a-thread
        Events()
        app = web.Application()
        sio_server.attach(app)
        runner = web.AppRunner(app)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        loop.create_task(self.send_tasks())
        loop.create_task(self.ping())
        command_line_interface.notify(f'Starting {self.NAME} on http://{arguments.ip}:{arguments.port}/', 'INFORMATION')
        try:
            if arguments.ssl:
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(arguments.ssl[0], arguments.ssl[1])
                site = web.TCPSite(runner, arguments.ip, arguments.port, ssl_context=ssl_context)
            else:
                site = web.TCPSite(runner, arguments.ip, arguments.port)
            loop.run_until_complete(site.start())
            loop.run_forever()
        except PermissionError:
            command_line_interface.notify(f'Failed to start {self.NAME} on port {arguments.port}: Permission Denied.', 'ERROR')