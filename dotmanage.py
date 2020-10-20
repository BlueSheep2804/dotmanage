import subprocess as subproc
import sys


def _check_git():
    if subproc.call('which git', shell=True) == 0:
        return True
    else:
        return False


def init():
    if not _check_git():
        return False

    print('Your dotfiles remote repository')
    print('e.g. git@github.com:BlueSheep2804/dotfiles')
    remote_uri = input('>> ')
    if not remote_uri:
        sys.exit(1)


print(sys.argv)
init()
