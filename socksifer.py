import argparse
import threading

from socksifer.cli import command_line_interface
from socksifer.constants import BANNER
from socksifer.flasksocketio import flasksocketio_server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=BANNER, formatter_class=argparse.RawTextHelpFormatter,
                                     usage=argparse.SUPPRESS)
    parser.add_argument('--ip', metavar='ip', help='Server ip.', default='127.0.0.1')
    parser.add_argument('--port', metavar='port', help='Server port.', default=1337)
    parser.add_argument('--ssl', nargs=2, metavar=('CERT', 'KEY'), help='Use SSL.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')
    threading.Thread(target=flasksocketio_server.run, daemon=True, args=(parser.parse_args(),)).start()
    command_line_interface.run()
