from cx_Freeze import setup, Executable


build_options = {'packages': [], 'excludes': []}


executables = [
        Executable('main.py', base='console', targetName= 'avtoskin.exe')
    ]

setup(name='avtoskin.exe',
        version='2.0.3',
        description='avtoskin',
        options={'build_exe': build_options},
        executables=executables)