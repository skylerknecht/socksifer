class Command:

    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def help(self):
        print(f'{self.description}\n')
        if not self.parameters:
            return
        print('parameters:')
        for parameter, description in self.parameters.items():
            print('{:<{}}{:<{}}{}'.format(' ', 4, parameter, 8, description))
        print(self.usage)

    @property
    def usage(self) -> str:
        return f"""
            No usage available for {self.name}.
        """

    def execute_command(self, parameters, notify):
        raise NotImplementedError(f'{self.name} command has not implemented execute_command')
