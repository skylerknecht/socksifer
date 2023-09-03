import socketio
import time

# standard Python
client = socketio.Client()

client.connect('http://localhost:8080')
print('my sid is', client.sid)


@client.event
def ping(data):
    the_time = int(data)
    print(time.time()-the_time)
    #time.sleep(1)
    client.emit('pong', time.time())

client.emit('pong', time.time())

while True:
    pass