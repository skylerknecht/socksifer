from .commands import Command
from socksifer import set_debug_level
from socksifer.output import display


class Debug(Command):
    def __init__(self):
        super().__init__(
            'debug',
            'Set the debug level.',
            {'level': 'The debug level'}
        )

    def execute_command(self, parameters, notify):
        if len(parameters) != 1:
            display('Invalid parameters.', 'ERROR')
            return
        try:
            level = int(parameters[0])
        except ValueError:
            display(f'{parameters[0]} is not an integer.', 'ERROR')
            return
        if 0 > level > 5:
            display(f'{level} is not between zero and five.', 'ERROR')
            return
        set_debug_level(level)
        display(f'Set the debug level to {level}', 'SUCCESS')