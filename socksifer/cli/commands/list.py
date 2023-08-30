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
                'proxying': str(socks_server.socks_server.proxy)
            })
        if len(socks_servers) == 0:
            display('There are no socks servers', 'INFORMATION')
            return
        display(self.create_table('SERVERS', ['id', 'address', 'port', 'proxying'], socks_servers))

    def create_table(self, title, columns: list, items: list[dict]) -> str:
        # ToDo: Pretty sure this logic is faulty if a column name is longer then one of the values. But meh.
        column_length = self.longest_value(items)
        title_padding = int(column_length / 2) * int(len(columns) / 2)
        table_output = f'{" " * title_padding}{title.upper()}\n'
        table_output += ' '.join('{:<{}}'.format(column, column_length) for column in columns) + '\n'
        table_seperator = '•' * column_length
        table_output += f'{table_seperator} ' * len(columns) + ' \n'
        table_output += '\n'.join(
            ' '.join('{:<{}}'.format(item[column], column_length) for column in columns) for item in items)
        return table_output

    @staticmethod
    def longest_value(items: list[dict]):
        return max(len(value) for item in items for value in item.values())