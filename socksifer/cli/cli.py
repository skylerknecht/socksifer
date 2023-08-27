import readline
import sys
import threading

from .commands import commands_manager
from socksifer.output import display


class CLI:

    def __init__(self, prompt):
        self.arguments = None
        self.output_lock = threading.Lock()
        self.output = []
        self.PROMPT = prompt
        self.prompt = self.PROMPT

    def listen_for_user_input(self):
        display('Welcome to the Socksifer CLI, type help or ? to get started')
        while True:
            try:
                with self.output_lock:
                    user_input = input('\r' + self.prompt)
                if not user_input:
                    continue
                commands_manager.execute_command(user_input, self.set_cli_properties, self.notify)
            except KeyboardInterrupt:
                display('')

    def notify(self, *args):
        display('\r', end='')
        display(*args)
        display(self.prompt + readline.get_line_buffer(), end='')
        sys.stdout.flush()

    def run(self, arguments=None):
        self.arguments = arguments
        self.listen_for_user_input()

    def set_cli_properties(self,prompt=None, reset: bool = False):
        if reset:
            self.prompt = self.PROMPT
            return
        self.prompt = prompt if prompt else self.prompt
