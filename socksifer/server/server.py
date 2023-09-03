import asyncio

from .events import Events
from aiohttp import web
from socksifer import sio_server
from socksifer.client import command_line_interface


class SocketIOServer:
    NAME = 'SocketIO Server'

    def __init__(self):
        pass

    def run(self, arguments):
        # https://stackoverflow.com/questions/51610074/how-to-run-an-aiohttp-server-in-a-thread
        Events()
        app = web.Application()
        sio_server.attach(app)
        runner = web.AppRunner(app)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runner.setup())
        command_line_interface.notify(f'Starting {self.NAME} on http://{arguments.ip}:{arguments.port}/', 'INFORMATION')
        try:
            #web.run_app(app, host=arguments.ip, port=arguments.port)
            site = web.TCPSite(runner, arguments.ip, arguments.port)
            loop.run_until_complete(site.start())
            loop.run_forever()
        except PermissionError:
            command_line_interface.notify(f'Failed to start {self.NAME} on port {arguments.port}: Permission Denied.', 'ERROR')
