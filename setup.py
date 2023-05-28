from cx_Freeze import setup, Executable
import sys

sys.argv = [sys.argv[0], 'build']

build_options = {'packages': [], 'excludes': []}


executables = [
        Executable('main.py', base='console', targetName= 'avtoskin.exe')
    ]

setup(name='avtoskin.exe',
        version='3.0',
        description='avtoskin',
        options={'build_exe': build_options},
        executables=executables)