class Command:

    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def help(self):
        print(f'{self.description}')
        if not self.parameters:
            return
        print('\nparameters:')
        for parameter, description in self.parameters.items():
            print('{:<{}}{:<{}}{}'.format(' ', 4, parameter, 8, description))
        if self.example: print(self.example)

    @property
    def example(self) -> str:
        return ''

    def execute_command(self, parameters, notify, set_cli_properties):
        raise NotImplementedError(f'{self.name} command has not implemented execute_command')
