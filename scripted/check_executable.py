"""
Ceci correspond à des tests sur l'exécutable final.
Puisqu'ils peuvent modifier le fichiers utilsateurs
il faut les utiliser qu'en intégration continue
"""

import subprocess
import platform
import logging
import sys
from pathlib import Path
from appdirs import user_cache_dir

logging.basicConfig()
LOG = logging.getLogger("testexec")
# test if  ddblocation removed

DDB = Path(user_cache_dir(), "MyDevoirs", "ddb_hard.sqlite")


def check_is_fresh_install():
    try:
        assert not DDB.exists()
    except AssertionError as e:
        LOG.error("not fress install")
        raise e


EXT = ".exe" if platform.system() == "Windows" else ""
BIN_NAME = "MyDevoirs" + EXT
BIN_PATH = Path(BIN_NAME).absolute() / BIN_NAME  #artifact does zip


def run_mydevoirs():

    proc = subprocess.Popen(
        [str(BIN_PATH)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        assert proc.poll() is None
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/IM", str(BIN_PATH)])
        else:
            proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            LOG.error("Echec de l'arret, essai kill")
            proc.kill()
        else:
            LOG.info("Execution sans erreur !!")

    else:
        LOG.error(
            """
            ###################################################################

                            Il y a eu un problème
            
            code de retour = %s

            Message d'erreur:
            %s""",
            proc.returncode,
            proc.stdout.read().decode(),
        )
        sys.exit(-1)


if __name__ == "__main__":
    LOG.info("execution fresh")
    check_is_fresh_install()
    run_mydevoirs()
    LOG.info("execution non fresh")
    run_mydevoirs()


# https://github.com/jgirardet/mydevoirs/releases/latest
