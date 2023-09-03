import base64
import json
import select
import socket
import socketio
import threading
import time
import sys

server_id = ''
sio = socketio.Client()
socks_connections = {}
upstream_buffer = {}


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
    global upstream_buffer
    data = json.loads(data)
    client_id = data['client_id']
    upstream_buffer[client_id].append(base64_to_bytes(data['data']))


def stream(client_id):
    global upstream_buffer
    while True:
        client = socks_connections[client_id]
        r, w, e = select.select([client], [client], [])
        if client in w and len(upstream_buffer[client_id]) > 0:
            client.send(upstream_buffer[client_id].pop(0))
        if client in r:
            try:
                downstream_data = client.recv(4096)
                if len(downstream_data) <= 0:
                    break
                socks_downstream_result = json.dumps({
                    'client_id': client_id,
                    'data': bytes_to_base64(downstream_data)
                })
                sio.emit('socks_downstream_results', socks_downstream_result)
            except:
                break




@sio.event
def socks_connect(data):
    global socks_connections
    data = json.loads(data)
    atype = data['atype']
    address = data['address']
    port = data['port']
    client_id = data['client_id']
    socks_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks_connection.settimeout(5.0)
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
        upstream_buffer[client_id] = []
        bind_addr = socks_connection.getsockname()[0]
        bind_port = socks_connection.getsockname()[1]
        results = json.dumps({
            'atype': atype,
            'rep': rep,
            'bind_addr': bind_addr,
            'bind_port': bind_port,
            'client_id': client_id
        })
        threading.Thread(target=stream, daemon=True, args=(client_id,)).start()
    sio.emit('socks_connect_results', results)


@sio.event
def ping(data):
    sio.emit('pong', data)


if len(sys.argv) != 2:
    print(f'Incorrect arguments provided. Please run {sys.argv[0]} http://server-url:port/')
    sys.exit()

sio.connect(sys.argv[1])