"""
Ceci correspond à des tests sur l'exécutable final.
Puisqu'ils peuvent modifier le fichiers utilsateurs
il faut les utiliser qu'en intégration continue
"""
import logging
import platform
import subprocess
import sys
from pathlib import Path

from appdirs import user_cache_dir

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
# test if  ddblocation removed

DDB = Path(user_cache_dir(), "MyDevoirs", "ddb_hard.sqlite")
ROOT = Path(__file__).parents[1]
APPNAME = "mydevoirs"


def check_is_fresh_install():
    try:
        assert not DDB.exists()
    except AssertionError as e:
        LOG.info("not fress install %s already exists", str(DDB))
    else:
        LOG.info(f"using existing {DDB}")


def get_executable():
    from briefcase.config import parse_config

    with open(ROOT / "pyproject.toml") as ff:
        _, appconfig = parse_config(ff, sys.platform, "")
    version = appconfig[APPNAME]["version"]
    if platform.system() == "Windows":
        exe = ["briefcase", "run"]
    else:
        exe = [
            Path(__file__).parents[1] / "linux" / f"{APPNAME}-{version}-x86_64.AppImage"
        ]
    return exe


def run_mydevoirs():
    exe = get_executable()
    LOG.info(f"runnung my devoirs with command {exe}")
    STARTUPINFO = None
    if platform.system == "Windows":
        STARTUPINFO = subprocess.STARTUPINFO()
        STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        STARTUPINFO.wShowWindow = subprocess.SW_HIDE
    proc = subprocess.Popen(
        exe,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        startupinfo=STARTUPINFO,
        cwd=ROOT,
    )

    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        assert proc.poll() is None
        LOG.info("execution sans problème après 10 secondes")
        proc.terminate()
        sys.exit(0)

    else:
        LOG.error("Le programme s'est intéromput plus tôt")
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            LOG.error("Le programme est bloqué")
            LOG.error(proc.stdout.read().decode())
            LOG.error(proc.stderr.read().decode())
            # on quite
        else:
            LOG.error("Message d'erreur")
            LOG.error(out.decode())
        sys.exit(-1)


if __name__ == "__main__":
    LOG.info(platform.system())
    check_is_fresh_install()
    run_mydevoirs()
    LOG.info("execution non fresh")
    run_mydevoirs()
    sys.exit(0)
