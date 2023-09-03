import time

from .commands import Command
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Socks(Command):
    def __init__(self):
        super().__init__(
            'socks',
            'List all of the socks proxies.',
            {}
        )

    def execute_command(self, parameters, notify, set_cli_properties):
        socks_servers = []
        for socks_server in socks_server_manager.socks_servers.values():
            listening = socks_server.socks_server.listening
            #print(listening)
            #print(socks_server.socks_server.latency)
            if socks_server.socks_server.latency:
                check_in_delta = (time.time() - socks_server.socks_server.check_in) - 1
                #print(check_in_delta)
                connected = listening and check_in_delta <= (socks_server.socks_server.latency * 3)
            else:
                connected = False
            socks_servers.append({
                'id': socks_server.socks_server.server_id,
                'connected': connected,
                'address': socks_server.socks_server.address,
                'port': str(socks_server.socks_server.port),
                'latency': self.latency_to_string(socks_server.socks_server.latency)
            })
        if len(socks_servers) == 0:
            display('There are no socks servers', 'INFORMATION')
            return
        display(self.create_table('SERVERS', socks_servers[0].keys(), socks_servers))

    @staticmethod
    def create_table(title, columns: list, items: list) -> str:
        # Calculate the maximum width for each column
        col_widths = [len(col) for col in columns]
        for item in items:
            for idx, col in enumerate(columns):
                col_widths[idx] = max(col_widths[idx], len(str(item.get(col, ''))) + 4)

        # Create the table header
        header = f"{title:^{sum(col_widths) + len(columns) - 1}}\n"
        header += ' '.join([f"{col:^{width}}" for col, width in zip(columns, col_widths)]) + '\n'
        header += ' '.join(['-' * width for width in col_widths]) + '\n'

        # Create the table rows
        rows = []
        for item in items:
            row = ' '.join([f"{str(item.get(col, '')):^{width}}" for col, width in zip(columns, col_widths)]) + '\n'
            rows.append(row)

        # Combine header and rows to form the table
        table = header + ''.join(rows)
        return table

    @staticmethod
    def latency_to_string(latency):
        if not latency:
            return '....'
        if latency < 1:
            return f'{int(latency * 1000)} ms'
        elif latency < 60:
            return f'{latency:.2f} second(s)'
        elif latency < 3600:
            return f'{latency / 60:.2f} minute(s)'
        else:
            return f'{latency / 3600:.2f} hour(s)'