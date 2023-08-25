import json
import random
import threading

from flask import request
from flask_socketio import disconnect, emit
from functools import wraps
from socksifer import get_debug_level
from socksifer import socketio as sio_server
from socksifer.cli import command_line_interface
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Events:

    def __init__(self):
        sio_server.on_event('connect', self.connect)
        sio_server.on_event('socks_request_for_data', self.socks)
        sio_server.on_event('socks_connect_results', self.socks_connect_results)
        sio_server.on_event('socks_downstream_results', self.socks_downstream_results)

    def connect(self):
        client_ip = request.remote_addr
        if get_debug_level() >= 1: command_line_interface.notify(f'{client_ip} attempting to authenticate', 'INFORMATION')
        if get_debug_level() >= 1: command_line_interface.notify(f'{client_ip} successfully authenticated.', 'SUCCESS')
        server_id = socks_server_manager.create_socks_server('127.0.0.1', random.randint(9050, 9100),
                                                             command_line_interface.notify)
        emit('socks', json.dumps({
                    'server_id': server_id
                }),
             broadcast=False)

    def json_event_handler(handler_function):
        @wraps(handler_function)
        def decorated_handler(self, *args):
            if not args:
                display(f'No results provided to {handler_function.__name__}.', 'ERROR')
                return
            try:
                deserialized_json = json.loads(args[0])
            except json.JSONDecodeError:
                display(f'Invalid JSON provided to {handler_function.__name__} event: {args[0]}', 'ERROR')
                return
            return handler_function(self, deserialized_json)

        return decorated_handler

    @json_event_handler
    def socks(self, data):
        socks_tasks = socks_server_manager.get_socks_tasks(data['server_id'])
        for socks_task in socks_tasks:
            emit(socks_task.event, socks_task.data, broadcast=False)  # ToDo: This still sends to everyone

    @json_event_handler
    def socks_connect_results(self, results):
        threading.Thread(
            target=socks_server_manager.handle_socks_task_results,
            args=('socks_connect', results,),
            daemon=True
        ).start()

    @json_event_handler
    def socks_downstream_results(self, results):
        threading.Thread(
            target=socks_server_manager.handle_socks_task_results,
            args=('socks_downstream', results,),
            daemon=True
        ).start()
