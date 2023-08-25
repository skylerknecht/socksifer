from collections import namedtuple
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
flask_app = Flask('Socksifer')
debug_level = 0


def set_debug_level(level: int):
    global debug_level
    debug_level = level


def get_debug_level():
    global debug_level
    return debug_level
