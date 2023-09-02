import json
import random
import threading
import time
import multiprocessing

from flask import request
from flask_socketio import disconnect, emit
from functools import wraps
from socksifer import socketio as sio_server
from socksifer.cli import command_line_interface
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Events:

    def __init__(self):
        sio_server.on_event('connect', self.connect)
        sio_server.on_event('disconnect', self.disconnect)
        sio_server.on_event('socks_request_for_data', self.socks)
        sio_server.on_event('socks_connect_results', self.socks_connect_results)
        sio_server.on_event('socks_downstream_results', self.socks_downstream_results)

    @staticmethod
    def connect():
        client_ip = request.remote_addr
        command_line_interface.notify(f'Connection request received from {request.sid} ({client_ip})', 'INFORMATION')
        command_line_interface.notify(f'Attempting to create socks server for {request.sid}', 'INFORMATION')
        socks_server_manager.create_socks_server(request.sid, '127.0.0.1', random.randint(9050, 9100),
                                                 command_line_interface.notify)

    @staticmethod
    def disconnect():
        if socks_server_manager.socks_servers[request.sid].socks_server.listening:
            socks_server_manager.shutdown_socks_server(request.sid, command_line_interface.notify)

    @staticmethod
    def socks():
        if not socks_server_manager.check_in_server(request.sid):
            disconnect()
            return
        socks_tasks = socks_server_manager.get_socks_tasks(request.sid)
        for socks_task in socks_tasks:
            emit(socks_task.event, socks_task.data, broadcast=False)  # ToDo: This still sends to everyone

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
