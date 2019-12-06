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
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
# test if  ddblocation removed

DDB = Path(user_cache_dir(), "MyDevoirs", "ddb_hard.sqlite")


def check_is_fresh_install():
    try:
        assert not DDB.exists()
    except AssertionError as e:
        LOG.error("not fress install %s already exists", str(DDB))
        sys.exit(-1)


EXT = ".exe" if platform.system() == "Windows" else ""
BIN_NAME = "MyDevoirs" + EXT
BIN_PATH = Path(BIN_NAME).absolute() / BIN_NAME  # artifact does zip


def run_mydevoirs():

    LOG.info("runnung my devoirs")
    proc = subprocess.Popen(
        str(BIN_PATH), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )

    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        LOG.info("execution sans problème après 10 secondes")
        assert proc.poll() is None
        # out, err = proc.communicate(timeout=5)
        LOG.info(proc.stdout.read().decode())
        LOG.info(proc.stderr.read().decode())
        sys.exit(0)

    else:
        try:
            out, err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            LOG.info(proc.stdout.read().decode())
            LOG.info(proc.stderr.read().decode())
            #on quite
        else:   
            LOG.info(out.decode())
            LOG.info(err.decode())
        # stdout = proc.stdout.read()
        # LOG.error(
        #     """
        #     ###################################################################

        #                     Il y a eu un problème
            
        #     code de retour = %s

        #     Message d'erreur:
        #     %s""",
        #     ret,
        #     stdout.decode(),
        # )
        sys.exit(-1)


if __name__ == "__main__":
    LOG.info(platform.system())
    LOG.info("ddb %s", str(DDB))
    LOG.info("ddb exists %s", DDB.exists())
    LOG.info("ddb parent (Mydevoirs) exists %s", DDB.parent.exists())
    LOG.info("ddb parent (Mydevoirs.parent) exists %s", DDB.parents[1].exists())
    LOG.info("execution fresh")
    check_is_fresh_install()
    run_mydevoirs()
    LOG.info("execution non fresh")
    run_mydevoirs()


# https://github.com/jgirardet/mydevoirs/releases/latest
