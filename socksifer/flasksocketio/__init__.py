import logging

from .flasksocketio import FlaskSocketIOServer

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
flasksocketio_server = FlaskSocketIOServer()
