from .debug import Debug
from .exit import Exit
from .socks import Socks
from .manager import CommandsManager
from .shutdown import Shutdown

debug = Debug()
exit = Exit()
socks = Socks()
shutdown = Shutdown()

commands = {
    debug.name: debug,
    exit.name: exit,
    socks.name: socks,
    shutdown.name: shutdown
}

commands_manager = CommandsManager(commands)