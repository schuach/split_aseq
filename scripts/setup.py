from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("split_aseq.py", base=base)]

packages = []
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "split_aseq",
    options = options,
    version = "0.1",
    description = 'splits aseq files in one file per record',
    executables = executables
)
