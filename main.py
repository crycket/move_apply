import argparse
import json

from src.interface import start

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='move_and_apply', usage='%(prog)s [path to settings.json]\nEx: %(prog)s ~/.ssh/settings.json',
        description='Creates diff from local repo and it applies it to remote repo.')
    parser.add_argument('settings', type=argparse.FileType('r'), default='~/.ssh/settings.json',
        help="""Json file path containing:\n{ "user": "username", "key_file": "path to id_rsa", "host": "host",
        "local_path": "local repo path", "remote_path": "remote repo path" }""")
    parser.add_argument('command', choices=['build', 'ut', 'mt', 'sct', 'lint'], help='command sent to mfo')
    args = parser.parse_args()
    settings = json.load(args.settings)
    print(settings)
    start(settings, args.command)

# /var/fpwork/crmocan/mfo/mfo --asap -Na x86_64 build
# /var/fpwork/crmocan/mfo/mfo --asap -Na x86_64 ut
# /var/fpwork/crmocan/mfo/mfo --asap -Na x86_64 mt
# /var/fpwork/crmocan/mfo/mfo -N cpplint