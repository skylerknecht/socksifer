from collections import namedtuple
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
flask_app = Flask('Socksifer')
