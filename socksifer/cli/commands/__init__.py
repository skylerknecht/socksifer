from .manager import CommandsManager
from .create import Create
from .exit import Exit
from .list import List
from .shutdown import Shutdown

create = Create()
exit = Exit()
list = List()
shutdown = Shutdown()

commands = {
    create.name: create,
    exit.name: exit,
    list.name: list,
    shutdown.name: shutdown
}

commands_manager = CommandsManager(commands)