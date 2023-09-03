import socketio

__version__ = '0.0.0'
debug_level = 0
sio_server = socketio.AsyncServer(async_mode='aiohttp')


def set_debug_level(level: int):
    global debug_level
    debug_level = level


def get_debug_level():
    global debug_level
    return debug_level
