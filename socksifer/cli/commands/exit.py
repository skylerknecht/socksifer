import sys

from .commands import Command


class Exit(Command):
    def __init__(self):
        super().__init__(
            'exit',
            'Exits the CLI.',
            {}
        )

    def execute_command(self, parameters, notify):
        sys.exit()
