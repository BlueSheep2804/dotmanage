import os
import subprocess
import sys
from pathlib import Path


def _check_git():
    if subprocess.call('type git', shell=True) == 0:
        return True
    else:
        return False


def init():
    if not _check_git():
        sys.exit(1)

    print('Your dotfiles remote repository')
    print('e.g. git@github.com:BlueSheep2804/dotfiles')
    remote_uri = input('>> ')
    if not remote_uri:
        sys.exit(1)
    subprocess.call(f'git remote set-url origin {remote_uri}', shell=True)

    if subprocess.check_output('git remote get-url origin', shell=True) == f'{remote_uri}\n'.encode():
        print('OK')
    else:
        sys.exit(1)

    print('Initialize successfully.')


def link():
    print('Create symbolic link.')

    home_files = Path(os.environ['HOME'])

    print('Target user home directory')
    print(f'{str(home_files)}')
    print('Are you sure?')
    inp = input('[y/N]>> ')
    if inp != 'y':
        sys.exit(1)

    files = Path('./home/').glob('**/*')

    for f in files:
        target_file = Path(f'{str(home_files)}/{str(f)[5:]}')
        if f.is_dir():
            os.makedirs(f'{target_file}', exist_ok=True)
        elif f.is_file():
            if target_file.exists():
                if target_file.is_symlink():
                    target_file.unlink()
                else:
                    print(f'{target_file} is exists.')
                    print('Replace it?')
                    inp = input('[Y/n]>> ')
                    _print_lineback(3)
                    if inp == 'n':
                        _print_color('[SKIP]', 36)
                        print(f' {target_file}')
                        continue
                    target_file.replace(f'{target_file}.backup')
                    _print_color('[BACKUP]', 34)
                    print(f' {target_file}.backup')
            target_file.symlink_to(f.resolve())
            _print_color('[LINK]', 32)
            print(f' {target_file}')


def version():
    _print_color('dotmanage.py', 36)
    print(' v0.1')


def help():
    version()
    print()

    _print_color('init', 32)
    print(': Initialize dotfiles git repository')

    _print_color('link', 32)
    print(': Link dotfiles')

    _print_color('version', 32)
    print(': Show dotmanage.py version')

    _print_color('help', 32)
    print(': Show this help message')


def _print_lineback(back_count: int):
    for i in range(back_count):
        print('\033[A\033[K', end='')


def _print_color(string: str, color: int):
    print(f'\033[{color}m{string}\033[0m', end='')


if sys.argv[1] == 'init':
    init()
elif sys.argv[1] == 'link':
    link()
elif sys.argv[1] == 'version':
    version()
elif sys.argv[1] == 'help':
    help()
