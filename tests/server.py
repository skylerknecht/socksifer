import socketio
import time
from aiohttp import web

# create a Socket.IO server
startup_time = time.time()
server = socketio.AsyncServer(async_mode='aiohttp', async_handlers=True)

@server.event
def connect(sid, environ, auth):
    print("I'm connected!")

@server.event
async def pong(sid, data):
    print(time.time() - data)
    await server.emit('ping', time.time())


app = web.Application()
server.attach(app)

if __name__ == '__main__':
    web.run_app(app)