import sys
import platform
import os
from pathlib import Path


def configure_env():
    if platform.system() == "Windows":  # pragma: no cover_linux
        os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"
        if Path(sys.executable).name == "pythonw.exe":
            os.environ["KIVY_NO_CONSOLELOG"] = "True"


if __name__ == "__main__":

    configure_env()

    from mydevoirs.main import main

    main()
