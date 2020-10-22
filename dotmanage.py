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

    for f in files:
        target_file = Path(f'{str(home_files)}/{str(f)[5:]}')
        if f.is_dir():
            os.makedirs(f'{str(home_files)}/{f.name}', exist_ok=True)
        elif f.is_file():
            if target_file.exists():
                if target_file.is_symlink():
                    target_file.unlink()
                else:
                    print(f'{target_file} is exists.')
                    print('Replace it?')
                    inp = input('[Y/n]>> ')
                    print('\033[3A\033[K', end='')
                    if inp == 'n':
                        print(f'\033[36m[SKIP]\033[0m {target_file}')
                        continue
                    target_file.replace(f'{target_file}.backup')
                    print(f'\033[34m[BACKUP]\033[0m {target_file}.backup')
            target_file.symlink_to(f.resolve())
            print(f'\033[32m[LINK]\033[0m {target_file}')


print(sys.argv)
link()
