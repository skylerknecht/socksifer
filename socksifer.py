import argparse
import sys
import threading

from socksifer import __version__ as version
from socksifer.cli import command_line_interface
from socksifer.constants import BANNER
from socksifer.flasksocketio import flasksocketio_server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=BANNER, formatter_class=argparse.RawTextHelpFormatter,
                                     usage=argparse.SUPPRESS)
    parser.add_argument('--ip', metavar='ip', help='server ip', default='127.0.0.1')
    parser.add_argument('--port', metavar='port', help='server port', default=1337)
    parser.add_argument('--version', action='store_true', help='display the current version')
    args = parser.parse_args()
    if args.version:
        print(version)
        sys.exit()
    threading.Thread(target=flasksocketio_server.run, daemon=True, args=(args,)).start()
    command_line_interface.run()
