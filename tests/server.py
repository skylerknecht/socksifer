import socketio
import time
from aiohttp import web

# create a Socket.IO server
startup_time = time.time()
server = socketio.AsyncServer(async_mode='aiohttp')

@server.event
def connect(sid, environ, auth):
    print("I'm connected!")

@server.event
async def kevin(sid, data):
    await server.sleep(2)
    print(f'event {data} at {int(time.time() - startup_time)} seconds after startup time')


app = web.Application()
server.attach(app)

if __name__ == '__main__':
    web.run_app(app)