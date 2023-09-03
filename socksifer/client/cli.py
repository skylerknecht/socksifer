import readline
import sys

from .commands import commands, commands_manager
from socksifer.output import display
from socksifer.socks import socks_server_manager


class CLI:

    def __init__(self, prompt):
        self.arguments = None
        self.output = []
        self.PROMPT = prompt
        self.prompt = self.PROMPT
        self.completer = Completer(commands)
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.completer.complete_option)
        readline.set_completer_delims(" \t\n\"\\'`@$><=;|&{(")

    def listen_for_user_input(self):
        display('Welcome to the socksiest proxy around, type help or ? to get started')
        while True:
            try:
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


class Completer:
    # ToDo: we need to change option to command - nomenclature
    def __init__(self, commands):
        self.commands = commands

    def complete_option(self, incomplete_option, state):
            '''
            Analyzes the length of current line buffer / incomplete_option and
            determines the user(s) completion.

            If the current line buffer is greater or equal to one and the current line
            buffer ends with a trailing space then that indicates the user is attempting
            to complete a multi-worded option. The length of the current line buffer,
            when delimeted by a space, must be incremented by one to correctly search
            for the next option.

            Otherwise, generate a list of all current menu options and file names that
            start with the current incomplete_option aka the last line in the buffer.

            Parameters:
                    incomplete_option (str()): The current incomplete option.
                    state (int()): An integer so that when the funciton is called
                                recursivley by readline it can gather all items
                                within the current finished_option list.

            Returns:
                    finished_option (str): Whatever option the callee has not
                                        gathered yet.
            '''
            current_line = readline.get_line_buffer()
            current_line_list = current_line.split()
            if len(current_line_list) >= 1 and current_line.endswith(' '):
                current_line_list.append('')
            finished_options = [command for command in self.commands | socks_server_manager.socks_servers.keys() if command.startswith(incomplete_option)]
            return finished_options[state]