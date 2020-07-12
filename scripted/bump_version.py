import subprocess
import sys
from pathlib import Path

import toml

GET_TAG = "git describe --tags $(git rev-list --tags --max-count=1)"
MODE = ["patch", "minor", "major", "prepatch", "preminor", "premajor", "prerelease"]
README = Path("README.md")

assert README.exists()


def get_tag():
    tag = subprocess.check_output(GET_TAG, shell=True).strip()
    return tag.decode()


def get_briefcase_version():
    version = toml.loads(open("pyproject.toml").read())["tool"]["briefcase"]["version"]
    return version


def update_doc_link(previous, new_version):
    readme = README.read_text()
    new = readme.replace(
        f"https://github.com/jgirardet/mydevoirs/releases/download/{previous}/",
        f"https://github.com/jgirardet/mydevoirs/releases/download/{new_version}/",
    )
    README.write_text(new)


if __name__ == "__main__":
    version = get_briefcase_version()
    tag = get_tag()
    if tag != version:
        raise EnvironmentError(
            f"Le numéro de version pyproject ({version}) et git ({tag}) ne correspondent pas."
        )

    mode = sys.argv[-1]
    if mode not in MODE:
        raise KeyError(f"argument {sys.argv[-1]} doit être un de {MODE}")

    new_version = (
        subprocess.check_output(f"poetry version {mode}", shell=True)
        .strip()
        .split()[-1]
        .decode()
    )

    print(f"updating doc with version {new_version}")
    update_doc_link(version, new_version)

    print(
        subprocess.check_output(f"git commit -a -m {new_version}", shell=True).decode()
    )
    print(subprocess.check_output(f"git tag {new_version}", shell=True).decode())

    assert get_tag() == get_briefcase_version()

    print(f"Nouvelle Version {new_version} !!!\n pushing")
    print(subprocess.check_output(f"git push", shell=True).decode())
    print(subprocess.check_output(f"git push --tags", shell=True).decode())
