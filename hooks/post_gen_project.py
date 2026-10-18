"""Make the new project a git repository.

setuptools-scm takes the version from git, so the project cannot be
installed before ``git init``.
"""

import shutil
import subprocess
import sys

if shutil.which("git") is None:
    print("git was not found: run 'git init' before installing the project.", file=sys.stderr)
else:
    subprocess.run(["git", "init", "--quiet"], check=True)
