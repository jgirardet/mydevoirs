import platform
from pathlib import Path
import PyInstaller.__main__
import shutil
import logging
import os

logging.basicConfig()
LOG = logging.getLogger(__name__)

WORKING_DIR = Path.cwd()
LOG.info(" working dir: %s", WORKING_DIR)
LOG.info("%s", os.listdir())
SPEC_NAME = "main_win.spec" if platform.system() == "Windows" else "main.spec"
LOG.info(SPEC_NAME)
SPEC_PATH = WORKING_DIR / SPEC_NAME
LOG.info(SPEC_PATH)

assert SPEC_PATH.is_file(), "spec path does not exists"
LOG.info("spec_path: %s", str(SPEC_PATH))


EXT = ".exe" if platform.system() == "Windows" else ""
BIN_NAME = "MyDevoirs" + EXT
DIST_PATH = WORKING_DIR / "dist"
BUILD_PATH = WORKING_DIR / "build"
BIN_PATH = (DIST_PATH / BIN_NAME).absolute()
LOG.info("bin_path: %s", str(BIN_PATH))

# cleanup previous
for rep in [DIST_PATH, BUILD_PATH]:
    if rep.is_dir():
        LOG.info("removing :%s", str(rep))
        shutil.rmtree(str(rep))


# build
PyInstaller.__main__.run(["-y", "--clean", str(SPEC_PATH)])
