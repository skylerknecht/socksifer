import socketio

# standard Python
client = socketio.Client()

client.connect('http://localhost:8080')


client.emit('kevin', '1')
client.emit('kevin', '2')
client.emit('kevin', '3')
print('my sid is', client.sid)

while True:
    pass