import ipaddress

from .commands import Command
from socksifer.output import display
from socksifer.socks import socks_server_manager


class Shutdown(Command):
    def __init__(self):
        super().__init__(
            'shutdown',
            'Shutdown a socks proxy.',
            {}
        )

    def execute_command(self, parameters, notify, set_cli_properties):
        if len(parameters) != 1:
            display('Invalid parameters.', 'ERROR')
            return

        socks_server_manager.shutdown_socks_server(parameters[0], notify)
