#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from shiv.bootstrap import Environment

# from distutils.ccompiler import new_compiler
from shiv.builder import create_archive
from shiv.cli import __version__ as VERSION


def build_nxc():
    print("building nxc")
    try:
        shutil.rmtree("bin")
        shutil.rmtree("build")
    except Exception as e:
        pass

    try:
        print("remove useless files")
        os.mkdir("build")
        os.mkdir("bin")
        shutil.copytree("nxc", "build/nxc")

    except Exception as e:
        print(e)
        return

    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-e",
            ".",
            "-t",
            "build",
        ],
        check=True,
    )

    # [shutil.rmtree(p) for p in Path("build").glob("**/__pycache__")]
    [shutil.rmtree(p) for p in Path("build").glob("**/*.dist-info")]

    env = Environment(
        built_at=datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"),
        entry_point="nxc.netexec:main",
        script=None,
        compile_pyc=False,
        extend_pythonpath=True,
        shiv_version=VERSION,
    )
    create_archive(
        [Path("build").absolute()],
        Path("bin/nxc"),
        "/usr/bin/env -S python -sE",
        "_bootstrap:bootstrap",
        env,
        True,
    )


def build_nxcdb():
    print("building nxcdb")
    env = Environment(
        built_at=datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"),
        entry_point="nxc.nxcdb:main",
        script=None,
        compile_pyc=False,
        extend_pythonpath=True,
        shiv_version=VERSION,
    )
    create_archive(
        [Path("build").absolute()],
        Path("bin/nxcdb"),
        "/usr/bin/env -S python -sE",
        "_bootstrap:bootstrap",
        env,
        True,
    )


if __name__ == "__main__":
    try:
        build_nxc()
        build_nxcdb()
    except:
        pass
    finally:
        shutil.rmtree("build")
