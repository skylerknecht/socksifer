import shlex

from socksifer.output import display


class CommandsManager:

    def __init__(self, commands):
        self.commands = commands

    def execute_command(self, user_input, set_cli_properties, notify):
        tokens = shlex.split(user_input)

        if len(tokens) <= 0:
            return

        if tokens[0] == '?':
            self.help_menu()
            return

        try:
            command = self.commands[tokens[0]]
        except KeyError:
            display(f'{tokens[0]} is not a valid command.', 'ERROR')
            return

        if '--help' in tokens or '-h' in tokens:
            command.help()
            return

        command.execute_command(tokens[1:], notify, set_cli_properties)

    def help_menu(self):
        for command in self.commands.values():
            print('{:<{}}{:<30}'.format(command.name, 10, command.description))