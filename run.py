import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
VIRTUAL_ENV = ROOT / ".venv"
PACKAGE_NAME = "mydevoirs"
currentProccess = None

OS = platform.system()


def get_env():
    env = os.environ
    path = env["PATH"]
    if OS == "Linux":
        new = f"{VIRTUAL_ENV / 'bin'}:"
    elif OS == "Windows":
        new = f"{VIRTUAL_ENV / 'Scripts'};"
    env["PATH"] = new + path
    return env


def get_shell():
    return os.environ.get("SHELL", None)


def get_dependencies():
    import toml

    pp = toml.load("pyproject.toml")
    app_pp = pp["tool"]["briefcase"]["app"][PACKAGE_NAME]
    p1 = app_pp["requires"]
    try:
        p2 = app_pp[OS.lower()]["requires"]
    except KeyError:
        p2 = []

    return p1 + p2


def cmd_rien(*args, **kwargs):
    runCommand("pip -V")


def runCommand(command, cwd=str(ROOT), sleep_time=0.2, with_env=True, exit=True):
    global currentProccess
    print(f"##### running: {command} #####")
    env = get_env() if with_env else None
    shell = True if sys.platform == "linux" else False
    process = subprocess.Popen(
        command,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        executable=get_shell(),
        cwd=cwd,
        env=env,
        universal_newlines=True,
    )
    currentProccess = process
    while process.poll() is None:
        for line in process.stdout:
            print(line, end="")
        time.sleep(sleep_time)
    if process.returncode == 0:
        print(
            f"##### finished: {command}  ==>>  OK  with return code {process.returncode} #####"
        )
        currentProccess = None
        return True
    else:
        print(
            f"##### finished: {command}  ==>>  ECHEC  with return code {process.returncode} #####"
        )
        if exit:
            return sys.exit(process.returncode)
        else:
            return False


def cmd_black(*args, **kwargs):
    import black

    if args:
        editedfile = Path(args[0])
        print(f"##### black formatting  {editedfile} #####")
        black.format_file_in_place(
            editedfile, fast=True, mode=black.FileMode(), write_back=black.WriteBack(1)
        )
    else:
        runCommand(f"python -m black {PACKAGE_NAME} tests")


def cmd_isort(*args, **kwargs):
    editedfile = Path(args[0]) if args else f"{PACKAGE_NAME} tests"
    runCommand(f"isort --profile black {editedfile}")


def cmd_style(*args, **kwargs):
    cmd_black(*args, **kwargs)
    cmd_isort(*args, **kwargs)


def cmd_clean(*args, **kwargs):
    to_remove = [
        *ROOT.rglob(".pytest_cache"),
        *ROOT.rglob("__pycache__"),
        *ROOT.rglob(".mypy_cache"),
        ROOT / "htmlcov",
        ROOT / "dist",
        ROOT / "aqtinstall.log",
        ".coverage",
        ROOT / "linux",
        ROOT / "windows",
    ]
    if "-venv" in args:
        to_remove.append(VIRTUAL_ENV)

    for p in to_remove:
        if isinstance(p, str):
            p = ROOT / p
        if p.is_dir():
            shutil.rmtree(p)
        elif p.is_file():
            p.unlink()


def cmd_cov(*args, **kwargs):
    pytest_cache = ROOT / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache)
    test_path = ROOT / "tests"
    runCommand(f"coverage run --rcfile=.coveragerc  -m pytest {test_path}")
    runCommand("coverage report")


def cmd_cov_html(*args, **kwargs):
    cmd_cov()
    runCommand("coverage html")
    html = ROOT / "htmlcov" / "index.html"
    runCommand(f"firefox {html} &")


def cmd_create(*args, **kwargs):
    cmd_clean()
    runCommand("briefcase create")
    if OS == "Windows":
        bundle = ROOT / "windows" / PACKAGE_NAME / "src"
        share = bundle / "app_packages" / "share"
        shutil.move(str(share.resolve()), str((bundle / "python").resolve()))


def cmd_create_env(*args, **kwargs):
    runCommand(f"{sys.executable} -m venv .venv", with_env=False)


def cmd_dev(*args, **kwargs):
    os.environ["MYDEVOIRS_DEBUG"] = "True"
    runCommand(f"briefcase dev")


def cmd_install(*args, **kwargs):
    runCommand(f"python -m pip install -U pip")
    runCommand(f"pip install -r requirements.txt")
    runCommand(f"python run.py install_from_require")


def cmd_install_from_require(*args, **kwargs):
    deps = [f'"{x}"' for x in get_dependencies()]
    runCommand(f"pip install {' '.join(deps)}")


def cmd_setup(*args, **kwargs):
    cmd_create_env(*args, *kwargs)
    cmd_install()


def cmd_version(*args, **kwargs):
    from briefcase.config import parse_config
    from git import Repo

    vcs = Repo(".")
    if vcs.is_dirty():
        raise EnvironmentError("Il reste des changements non validés")

    if vcs.active_branch.name != "master":
        raise EnvironmentError("Le changement de version doit s'effectuer sur master")

    with open("pyproject.toml") as ff:
        _, appconfig = parse_config(ff, sys.platform, "")
    version = appconfig[PACKAGE_NAME]["version"]
    vcs.create_tag(version)
    print(f"tag {version} créé")


def cmd_test(*args, **kwargs):
    runCommand(f"pytest -s -vvv tests", sleep_time=0.001)


def cmd_test_executable(*args, **kwargs):
    path = ROOT / "scripted" / "check_executable.py"
    runCommand(f"{sys.executable}  {path}")


def cmd_run(*args, **kwargs):
    runCommand("briefcase run -u")


def build_commands(*args, **kwargs):
    res = {}
    for i, j in globals().items():
        if callable(j) and i.startswith("cmd_"):
            res[i[4:]] = j
    return res


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("args", nargs="*")
    parser.add_argument("-input", nargs="?")
    parser.add_argument("-venv", nargs="?")
    parser.add_argument("-ni", "--no-input")

    args = parser.parse_args()
    com = args.command
    arguments = args.args

    try:
        commands = build_commands()
        if com not in commands:
            print(f"commandes possible : {list(commands.keys())}")
            sys.exit(1)
        commands[com](*arguments, input=args.input)
    except KeyboardInterrupt:
        currentProccess.terminate()
        sys.exit(0)
