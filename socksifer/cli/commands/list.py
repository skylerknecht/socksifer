import ipaddress

from .commands import Command
from socksifer.output import display
from socksifer.socks import socks_server_manager


class List(Command):
    def __init__(self):
        super().__init__(
            'list',
            'List all of the socks proxies.',
            {}
        )

    def execute_command(self, parameters, notify, set_cli_properties):
        socks_servers = []
        for socks_server in socks_server_manager.socks_servers.values():
            socks_servers.append({
                'id': socks_server.socks_server.server_id,
                'address': socks_server.socks_server.address,
                'port': str(socks_server.socks_server.port),
                'listening': str(socks_server.socks_server.listening)
            })
        if len(socks_servers) == 0:
            display('There are no socks servers', 'INFORMATION')
            return
        display(self.create_table('SERVERS', ['id', 'address', 'port', 'listening'], socks_servers))

    @staticmethod
    def create_table(title, columns: list, items: list[dict]) -> str:
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