"""
Ceci correspond à des tests sur l'exécutable final.
Puisqu'ils peuvent modifier le fichiers utilsateurs
il faut les utiliser qu'en intégration continue
"""

import subprocess
from build_executable import BIN_PATH, BIN_NAME
import platform
import logging
import sys
from pathlib import Path

logging.basicConfig()
LOG = logging.getLogger(__name__)
# test if  ddblocation removed


def test_is_fresh_install():
    # remove user disr
    from main import get_database_location

    assert not Path(get_database_location()).exists()


# test exec


def run_mydevoirs():

    proc = subprocess.Popen(
        str(BIN_PATH), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        assert proc.poll() is None
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/IM", BIN_NAME])
        else:
            proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            LOG.error("Echec de l'arret, essai kill")
            proc.kill()
        else:
            assert proc.poll() == 0
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
    test_is_fresh_install()
    run_mydevoirs()
    LOG.info('execution non fresh')
    run_mydevoirs()
