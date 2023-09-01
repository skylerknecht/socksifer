import textwrap
import time

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

    def execute_command(self, parameters, notify, set_cli_properties):
        if len(parameters) != 1:
            self.help()
            return
        try:
            level = int(parameters[0])
        except ValueError:
            display(f'{parameters[0]} is not an integer.', 'ERROR')
            return
        if not 0 <= level <= 5:
            display(f'{level} is not between zero and five.', 'ERROR')
            return
        if level == 5:
            for index in range(1, 10):
                print(f'computing{"." * index}', end='\r')
                time.sleep(.1)
            print(f'\033[2K\rno')
            return
        set_debug_level(level)
        display(f'Set the debug level to {level}', 'SUCCESS')

    @property
    def example(self):
        return textwrap.dedent('''
        debug levels:        
            1: socks_connect, client started streaming and stopped streaming.
            2: socks_connect data
            3: socks_upstream and socks_downstream
            4: socks_upstream and socks_downstream data
            5: socks around and find out\
        ''')
