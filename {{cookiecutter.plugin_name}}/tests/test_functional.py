"""Run each file in tests/functional with the plugin loaded.

Each ``.py`` file marks the lines where a message is expected with a
``# [message-symbol]`` comment. The ``.txt`` file next to it holds the full
expected output. To write the ``.txt`` files again from what pylint
outputs now, run::

    python tests/test_functional.py --update-functional-output

Upsides:

- pylint runs as your users run it: with all its checkers, the plugin loaded
  through its ``register`` function, and the options of the ``.rc`` file.
- Each test is a plain Python file, easy to write and to read.
- The whole output is checked: a message you did not expect, from your
  checker or from another one, makes the test fail.

Downsides:

- It is slower: each file goes through all of pylint.
- When a test fails, the problem can be far from the message, and harder to
  follow in a debugger.

The unit tests next to this file are faster. Use functional tests to show
what your checker does, and unit tests for small cases you want to check
quickly.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from _pytest.config import Config
from pylint.testutils import UPDATE_FILE, UPDATE_OPTION
from pylint.testutils.functional import (
    FunctionalTestFile,
    LintModuleOutputUpdate,
    get_functional_test_files_from_directory,
)
from pylint.testutils.lint_module_test import LintModuleTest

if TYPE_CHECKING:
    from pylint.lint import PyLinter

FUNCTIONAL_DIR = Path(__file__).parent.resolve() / "functional"


class _LoadPluginMixin:  # pylint: disable=too-few-public-methods
    """Load the plugin into the linter used by the test."""

    _linter: PyLinter

    def __init__(self, test_file: FunctionalTestFile, config: Config | None = None) -> None:
        super().__init__(test_file, config)  # type: ignore[call-arg]
        self._linter.load_plugin_modules(["{{ cookiecutter.module_name }}"])
        self._linter.load_plugin_configuration()


class PluginLintModuleTest(_LoadPluginMixin, LintModuleTest):
    """Check the output of pylint against the expected ``.txt`` file."""


class PluginLintModuleOutputUpdate(_LoadPluginMixin, LintModuleOutputUpdate):
    """Write the output of pylint to the expected ``.txt`` file."""


@pytest.mark.parametrize(
    "test_file",
    get_functional_test_files_from_directory(FUNCTIONAL_DIR),
    ids=lambda x: x.base,
)
def test_functional(test_file: FunctionalTestFile) -> None:
    """Lint one functional test file with the plugin loaded."""
    __tracebackhide__ = True  # pylint: disable=unused-variable
    lint_test: LintModuleTest
    if UPDATE_FILE.exists():
        lint_test = PluginLintModuleOutputUpdate(test_file)
    else:
        lint_test = PluginLintModuleTest(test_file)
    lint_test.setUp()
    lint_test.runTest()


if __name__ == "__main__":
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    try:
        sys.exit(pytest.main([__file__, *sys.argv[1:]]))
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
