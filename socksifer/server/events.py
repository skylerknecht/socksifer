import asyncio
import json
import random
import threading

from functools import wraps
from socksifer import sio_server
from socksifer.client import command_line_interface
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Events:

    def __init__(self):
        sio_server.on('connect', self.connect)
        sio_server.on('disconnect', self.disconnect)
        sio_server.on('pong', self.pong)
        sio_server.on('socks_connect_results', self.socks_connect_results)
        sio_server.on('socks_downstream_results', self.socks_downstream_results)

    @staticmethod
    def connect(sid, environ, _):
        socksifer_client_ip = environ['REMOTE_ADDR']
        command_line_interface.notify(
            f'Socksifer Client ({socksifer_client_ip}) connection request received assigning {sid} to the connection.',
            'INFORMATION')
        command_line_interface.notify(f'Attempting to create socks server for {sid}', 'INFORMATION')
        socks_server_manager.create_socks_server(sid, '127.0.0.1', random.randint(9050, 9100),
                                                 command_line_interface.notify)

    @staticmethod
    def disconnect(sid):
        socks_server_manager.shutdown_socks_server(sid, command_line_interface.notify)

    @staticmethod
    def pong(sid):
        if not socks_server_manager.check_in_server(sid):
            sio_server.disconnect(sid)
            return

    def json_event_handler(handler_function):
        @wraps(handler_function)
        def decorated_handler(self, *args):
            if not args:
                display(f'No results provided to {handler_function.__name__}.', 'ERROR')
                return
            try:
                deserialized_json = json.loads(args[-1])
            except json.JSONDecodeError:
                display(f'Invalid JSON provided to {handler_function.__name__} event: {args[0]}', 'ERROR')
                return
            return handler_function(self, deserialized_json)

        return decorated_handler

    @json_event_handler
    def socks_connect_results(self, results):
        threading.Thread(
            target=socks_server_manager.handle_socks_task_results,
            args=('socks_connect', results,),
            daemon=True
        ).start()

    @json_event_handler
    def socks_downstream_results(self, results):
        socks_server_manager.handle_socks_task_results('socks_downstream', results)
