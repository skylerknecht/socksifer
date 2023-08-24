import ipaddress

from .commands import Command
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Create(Command):
    def __init__(self):
        super().__init__(
            'create',
            'Create a socks proxy.',
            {}
        )

    def execute_command(self, parameters, notify):
        if len(parameters) != 2:
            display('Invalid parameters.', 'ERROR')
            return

        try:
            ipaddress.IPv4Address(parameters[0])
        except ipaddress.AddressValueError:
            display('Invalid IPv4 address.', 'ERROR')
            return

        try:
            parameters[1] = int(parameters[1])
        except ValueError:
            display('Port must be of type integer.', 'ERROR')
            return

        socks_server_manager.create_socks_server(parameters[0], parameters[1], notify)
