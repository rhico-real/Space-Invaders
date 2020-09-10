from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Space Invaders",
    options = options,
    version = "Version: 1",
    description = 'Space Invaders',
    executables = executables
)