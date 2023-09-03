import threading
import time

from collections import namedtuple
from .socks import SocksServer


class SocksManager:
    socks_server = namedtuple('SocksServer', ['socks_server_thread', 'socks_server'])

    def __init__(self):
        self.socks_servers = {}

    def check_in_server(self, server_id, latency):
        socks_server = self.socks_servers[server_id].socks_server
        if not socks_server.listening:
            return False
        if not socks_server.check_in:
            socks_server.check_in = time.time()
        else:
            socks_server.latency = latency
            socks_server.check_in = time.time()
        return True

    def create_socks_server(self, *args):
        new_socks_server = SocksServer(*args)
        socks_server_thread = threading.Thread(target=new_socks_server.listen_for_clients, daemon=True)
        socks_server_thread.start()
        self.socks_servers[new_socks_server.server_id] = self.socks_server(socks_server_thread, new_socks_server)

    def shutdown_socks_server(self, server_id, notify):
        try:
            _socks_server = self.socks_servers[server_id]
        except KeyError:
            notify(f'{server_id} is not a valid server id.', 'ERROR')
            return
        if not _socks_server.socks_server.listening:
            return
        _socks_server.socks_server.shutdown()
        _socks_server.socks_server_thread.join()
        notify(f'{server_id} successfully shutdown', 'SUCCESS')

    def shutdown_socks_servers(self):
        for socks_server in self.socks_servers:
            socks_server.socks_server.shutdown()
            socks_server.socks_server_thread.join()

    def handle_socks_task_results(self, method, results):
        for socks_server in self.socks_servers.values():
            for socks_client in socks_server.socks_server.socks_clients:
                if socks_client.client_id == results['client_id']:
                    if method == 'socks_connect':
                        socks_client.handle_socks_connect_results(results)
                    if method == 'socks_downstream':
                        socks_client.handle_socks_downstream_results(results)

    def server_is_listening(self, sever_id):
        return self.socks_servers[sever_id].socks_server.listening

    def get_socks_tasks(self, server_id):
        sent_socks_task = []
        for socks_server in self.socks_servers.values():
            if socks_server.socks_server.server_id == server_id:
                for socks_client in socks_server.socks_server.socks_clients:
                    while socks_client.socks_tasks:
                        sent_socks_task.append(socks_client.socks_tasks.pop(0))
        return sent_socks_task