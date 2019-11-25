from subprocess import run
import os
from pathlib import Path
import urllib.request

WINDOWS_DEP = [
    "docutils",
    "pygments",
    "pypiwin32",
    "kivy_deps.sdl2==0.1.22",
    "kivy_deps.glew==0.1.12",
    "kivy_deps.gstreamer==0.1.17",
    "kivy_deps.angle==0.1.9",
    "pywin32-ctypes",
    "pefile",
]


def set_poetry__path():
    if platfor
    os.environ["PATH"] = os.environ["PATH"] + ";" + str(Path.home() / ".poetry" / "bin")
    os.environ["PATH"] = os.environ["PATH"] + ";" + str(Path.home() / ".poetry" / "bin")


def set_poetry_linux_path():

def install_poetry():
    poetry_stream = urllib.request.urlopen('https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py')
    p= Path('getpoetry.py')
    p.write_bytes(poetry_stream.read())
    run(['python', str(p), "-y"])
    p.unlink()

"""
run('python -m pip install -U pip
        python -c "import urllib;a = ;open('get-poetry.py','wt').write(a.read().decode())"
        python get-poetry.py -y
        $ENV:PATH="$ENV:PATH;$ENV:USERPROFILE\.poetry\bin"
        poetry run python -m pip install -U pip
        poetry run python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.22 kivy_deps.glew==0.1.12 kivy_deps.gstreamer==0.1.17 kivy_deps.angle==0.1.9 pywin32-ctypes pefile
        poetry install')
"""

if __name__ == '__main__':

    # install_poetry()