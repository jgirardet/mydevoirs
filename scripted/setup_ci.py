import subprocess
import os
from pathlib import Path
import urllib.request
import platform


def run(arg):
    subprocess.run(arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def get_platform():
    if platform.system() == "Windows":
        return False, True
    elif platform.system() == "Linux":
        return True, False


LINUX, WIN = get_platform()


WIN_DEP = [
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


def set_poetry_path():
    sep = ";" if WIN else ":"
    os.environ["PATH"] = os.environ["PATH"] + sep + str(Path.home() / ".poetry" / "bin")


def install_poetry():
    poetry_stream = urllib.request.urlopen(
        "https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py"
    )
    p = Path("getpoetry.py")
    p.write_bytes(poetry_stream.read())
    run(["python", str(p), "-y"])
    p.unlink()



def update_pip():
    run("python -m pip install -U pip".split())


def pre_install_dep():
    dep = WIN_DEP if WIN else []
    cmd = ["pip", "install"] + dep
    run(cmd)


def install_package():
    run(["poetry", "install"])


def setup_env():
    update_pip()
    install_poetry()
    set_poetry_path()
    pre_install_dep()


if __name__ == "__main__":
    setup_env()
