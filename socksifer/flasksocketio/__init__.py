import logging

from .flasksocketio import FlaskSocketIOServer

log = logging.getLogger('werkzeug')
log.disabled = True
flasksocketio_server = FlaskSocketIOServer()
