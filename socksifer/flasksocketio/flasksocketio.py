import flask.cli
import os
import threading

from .events import Events
from socksifer import flask_app
from socksifer import socketio as sio_server
from socksifer.cli import command_line_interface
from socksifer.generate import string_identifier


class FlaskSocketIOServer:
    NAME = 'SocketIO Server'

    def __init__(self):
        self.authentication_key = string_identifier()

    def run(self, arguments):
        flask_app.config.from_pyfile(f'{os.getcwd()}/socksifer/flasksocketio/settings.py')
        flask.cli.show_server_banner = lambda *args: None
        Events(self.authentication_key)
        sio_server.init_app(flask_app)
        command_line_interface.notify(f'Starting {self.NAME} on {arguments.ip}:{arguments.port}', 'INFORMATION')
        command_line_interface.notify(f'The super secret key `{self.authentication_key}`', 'INFORMATION')
        try:
            sio_server.run(flask_app, host=arguments.ip, port=arguments.port)
        except PermissionError:
            command_line_interface.notify(f'Failed to start {self.NAME} on port {arguments.port}: Permission Denied.', 'ERROR')