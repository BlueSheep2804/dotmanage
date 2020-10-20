import os
import subprocess
import sys
from pathlib import Path


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

    home_files = Path(os.environ['HOME'])

    print('Target user home directory')
    print(f'{str(home_files)}')
    print('Are you sure?')
    inp = input('[y/N]>> ')
    if inp != 'y':
        sys.exit(1)

    files = Path('./home/').glob('**/*')

    for f in files:  # TODO: ファイル存在時の例外をキャッチする
        print(f.resolve())
        print(f'{str(home_files)}/{str(f)[5:]}')
        if f.is_dir():
            os.makedirs(f'{str(home_files)}/{f.name}', exist_ok=True)
        elif f.is_file():
            pass
            os.symlink(f.resolve(), f'{str(home_files)}/{str(f)[5:]}')



print(sys.argv)
link()
