import os
import subprocess
import sys


def _check_git():
    if subprocess.call('which git', shell=True) == 0:
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

    if subprocess.check_output('git remote get-url origin', shell=True) == remote_uri:
        print('OK')
    else:
        sys.exit(1)

    print('Initialize successfully.')


def link():
    print('Create symbolic link.')

    print('Target user home directory')
    print(f'[{os.environ['HOME']}]')
    print('Are you sure?')
    inp = input('[y/N]>> ')
    if inp != 'y':
        sys.exit(1)


print(sys.argv)
