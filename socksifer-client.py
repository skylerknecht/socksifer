import base64
import json
import select
import socket
import socketio
import threading
import time

server_id = ''
sio = socketio.Client()
socks_connections = {}
client_lock = threading.Lock()



def base64_to_bytes(data) -> bytes:
    """
    Base64 encode a bytes object.
    :param data: A base64 string.
    :return: A bytes object.
    :rtype: bytes
    """
    return base64.b64decode(data)


def bytes_to_base64(data) -> str:
    """
    Base64 encode a bytes object.
    :param data: A python bytes object.
    :return: A base64 encoded string
    :rtype: str
    """
    return base64.b64encode(data).decode('utf-8')


@sio.event
def socks(data):
    global server_id
    data = json.loads(data)
    server_id = data['server_id']


@sio.event
def socks_upstream(data):
    global socks_connections
    data = json.loads(data)
    client_id = data['client_id']
    client = socks_connections[client_id]
    try:
        with client_lock:
            client.sendall(base64_to_bytes(data['data']))
    except:
        return


def downstream(client_id):
    while True:
        time.sleep(0.0001)
        client = socks_connections[client_id]
        r, w, e = select.select([client], [], [], 1)
        if client in r:
            try:
                with client_lock:
                    downstream_data = client.recv(4096)
                if len(downstream_data) <= 0:
                    return
                socks_downstream_result = json.dumps({
                    'client_id': client_id,
                    'data': bytes_to_base64(downstream_data)
                })
                sio.emit('socks_downstream_results', socks_downstream_result)
            except:
                return

@sio.event
def socks_connect(data):
    global socks_connections
    data = json.loads(data)
    atype = data['atype']
    address = data['address']
    port = data['port']
    client_id = data['client_id']
    socks_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks_connection.settimeout(5)
    rep = None
    try:
        socks_connection.connect((address, port))
        rep = 0
    except socket.error as e:
        if e.errno == socket.errno.EACCES:
            rep = 2
        elif e.errno == socket.errno.ENETUNREACH:
            rep = 3
        elif e.errno == socket.errno.EHOSTUNREACH:
            rep = 4
        elif e.errno == socket.errno.ECONNREFUSED:
            rep = 5
        rep = rep if rep else 6

    if rep != 0:
        results = json.dumps({
            'atype': atype,
            'rep': rep,
            'bind_addr': None,
            'bind_port': None,
            'client_id': client_id
        })
    else:
        socks_connections[client_id] = socks_connection
        bind_addr = socks_connection.getsockname()[0]
        bind_port = socks_connection.getsockname()[1]
        results = json.dumps({
            'atype': atype,
            'rep': rep,
            'bind_addr': bind_addr,
            'bind_port': bind_port,
            'client_id': client_id
        })
    sio.emit('socks_connect_results', results)
    threading.Thread(target=downstream, daemon=True, args=(client_id,)).start()


sio.connect('http://127.0.0.1:1337/', auth='rgASTytIsa')

while True:
    time.sleep(0.001)
    if server_id:
        data = json.dumps({
            'server_id': server_id
        })
        sio.emit('socks_request_for_data', data)




