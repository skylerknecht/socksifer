from .debug import Debug
from .exit import Exit
from .list import List
from .manager import CommandsManager
from .shutdown import Shutdown

debug = Debug()
exit = Exit()
list = List()
shutdown = Shutdown()

commands = {
    debug.name: debug,
    exit.name: exit,
    list.name: list,
    shutdown.name: shutdown
}

commands_manager = CommandsManager(commands)