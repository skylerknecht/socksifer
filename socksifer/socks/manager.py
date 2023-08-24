
import threading

from collections import namedtuple
from socksifer.output import display
from .socks import SocksServer


class SocksManager:
    socks_server = namedtuple('SocksServer', ['socks_server_thread', 'socks_server'])

    def __init__(self):
        self.socks_servers = {}

    def create_socks_server(self, *args):
        new_socks_server = SocksServer(*args)
        socks_server_thread = threading.Thread(target=new_socks_server.listen_for_clients)
        socks_server_thread.daemon = True
        socks_server_thread.start()
        self.socks_servers[new_socks_server.server_id] = self.socks_server(socks_server_thread, new_socks_server)
        return new_socks_server.server_id

    def shutdown_socks_server(self, server_id):
        try:
            _socks_server = self.socks_servers[server_id]
        except KeyError:
            display(f'Socks server with id {server_id} does not exist.', 'ERROR')
            return
        _socks_server.socks_server.shutdown()
        _socks_server.socks_server_thread.join()
        display(f'Successfully shutdown socks server {server_id}', 'SUCCESS')

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

    def get_socks_tasks(self, server_id):

        sent_socks_task = []
        for socks_server in self.socks_servers.values():

            if socks_server.socks_server.server_id == server_id:
                for socks_client in socks_server.socks_server.socks_clients:
                    if socks_client.socks_tasks:
                        print(self.socks_servers.values())
                        print(server_id)
                        print(socks_client.socks_tasks)
                    while socks_client.socks_tasks:
                        sent_socks_task.append(socks_client.socks_tasks.pop(0))
        return sent_socks_task
