import json
import select
import socket
import threading
import time

from collections import namedtuple
from socksifer.convert import bytes_to_base64, base64_to_bytes
from socksifer.generate import string_identifier
from socksifer.output import display


class SocksClient:
    REPLIES = {
        0: 'succeeded',
        1: 'general SOCKS server failure',
        2: 'connection not allowed by ruleset',
        3: 'Network unreachable',
        4: 'Host unreachable',
        5: 'Connection refused',
        6: 'TTL expired',
        7: 'Command not supported',
        8: 'Address type not supported',
        **{i: 'unassigned' for i in range(9, 256)}
    }
    SOCKS_VERSION = 5

    def __init__(self, client, notify):
        self.atype_functions = {
            b'\x01': self._parse_ipv4_address,
            b'\x03': self._parse_domain_name,
            b'\x04': self._parse_ipv6_address
        }
        self.client = client
        self.client_id = string_identifier()
        self.notify = notify
        self.socks_task = namedtuple('SocksTask', ['event', 'data'])
        self.socks_tasks = []
        self.streaming = False

    def generate_reply(self, atype, rep, address, port):
        reply = b''.join([
            self.SOCKS_VERSION.to_bytes(1, 'big'),
            int(rep).to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            int(atype).to_bytes(length=1, byteorder='big'),
            socket.inet_aton(address) if address else int(0).to_bytes(1, 'big'),
            port.to_bytes(2, 'big') if port else int(0).to_bytes(1, 'big')
        ])
        return reply

    def parse_address(self):
        atype = self.client.recv(1)
        try:
            address, port = self.atype_functions.get(atype)(), int.from_bytes(self.client.recv(2), 'big', signed=False)
            return atype, address, port
        except KeyError:
            self.client.sendall(self.generate_reply(str(int.from_bytes(atype, byteorder='big')), 8, None, None))
            return None, None, None

    def _parse_ipv4_address(self):
        return socket.inet_ntoa(self.client.recv(4))

    def _parse_ipv6_address(self):
        ipv6_address = self.client.recv(16)
        return socket.inet_ntop(socket.AF_INET6, ipv6_address)

    def _parse_domain_name(self):
        domain_length = self.client.recv(1)[0]
        domain_name = self.client.recv(domain_length).decode('utf-8')
        return domain_name

    def negotiate_cmd(self):
        ver, cmd, rsv = self.client.recv(3)
        return cmd == 1

    def negotiate_method(self):
        ver, nmethods = self.client.recv(2)

        methods = [ord(self.client.recv(1)) for _ in range(nmethods)]
        if 0 not in methods:
            self.client.sendall(bytes([self.SOCKS_VERSION, int('FF', 16)]))
            return False

        self.client.sendall(bytes([self.SOCKS_VERSION, 0]))
        return True

    def proxy(self):
        if not self.negotiate_method():
            display('Socks client failed to negotiate method.', 'ERROR')
            self.client.close()
            return
        if not self.negotiate_cmd():
            display('Socks client failed to negotiate cmd.', 'ERROR')
            self.client.close()
            return
        atype, address, port = self.parse_address()
        if not address:
            display('Socks client failed to negotiate address.', 'ERROR')
            self.client.close()
            return
        data = json.dumps({
            'atype': int.from_bytes(atype, byteorder='big'),
            'address': address,
            'port': port,
            'client_id': self.client_id
        })
        self.socks_tasks.append(self.socks_task('socks_connect', data))

    def stream(self):
        self.streaming = True
        print('streaming..')
        while self.streaming:
            r, w, e = select.select([self.client], [self.client], [])
            while self.client in r:
                try:
                    data = self.client.recv(4096)
                    if len(data) <= 0:
                        break
                    socks_upstream_task = json.dumps({
                        'client_id': self.client_id,
                        'data': bytes_to_base64(data)
                    })
                    self.socks_tasks.append(self.socks_task('socks_upstream', socks_upstream_task))
                except Exception as e:
                    break
        print('not streaming..')
        self.streaming = False
        self.client.close()

    def handle_socks_connect_results(self, results):
        atype = results['atype']
        rep = results['rep']
        bind_addr = results['bind_addr'] if results['bind_addr'] else None
        bind_port = int(results['bind_port']) if results['bind_port'] else None
        try:
            self.client.sendall(self.generate_reply(atype, rep, bind_addr, bind_port))
        except socket.error as e:
            print("Could not send sock_connect:", e)
            return
        self.stream()

    def handle_socks_downstream_results(self, results):
        try:
            self.client.sendall(base64_to_bytes(results['data']))
        except:
            return


class SocksServer:
    proxy = True
    socks_client = namedtuple('SocksClient', ['thread', 'socks_client'])
    socks_clients = []

    def __init__(self, address, port, notify):
        self.address = address
        self.notify = notify
        self.port = port
        self.server_id = string_identifier()

    def listen_for_clients(self):
        socks_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socks_server.bind((self.address, self.port))
        except Exception as e:
            self.notify(f'Failed to start socks server', 'ERROR')
            self.proxy = False
        socks_server.settimeout(1.0)
        socks_server.listen(5)
        if self.proxy:
            self.notify(f'Successfully created socks server: {self.address}:{self.port}', 'SUCCESS')
        while self.proxy:
            try:
                client, addr = socks_server.accept()
            except socket.error as e:
                continue
            socks_client = SocksClient(client, self.notify)
            socks_client_thread = threading.Thread(target=socks_client.proxy, daemon=True)
            socks_client_thread.start()
            self.socks_clients.append(self.socks_client(socks_client_thread, socks_client))
        socks_server.close()

    def shutdown(self):
        for socks_client in self.socks_clients:
            socks_client.socks_client.stream = False
            socks_client.thread.join()
        self.proxy = False
