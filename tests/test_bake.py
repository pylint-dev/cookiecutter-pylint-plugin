"""Generate projects from the template and check that they work."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_tests(project_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run all the tests of the project, as ``pytest`` would."""
    return run(project_path, "-m", "pytest", *args)


def run_functional_tests(project_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run ``tests/test_functional.py`` as a script, which can update the outputs."""
    return run(project_path, "tests/test_functional.py", *args)


def run(project_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    # The plugin is imported from the project root instead of being installed.
    return subprocess.run(
        [sys.executable, *args, "-p", "no:cacheprovider"],
        cwd=project_path,
        env={**os.environ, "PYTHONPATH": str(project_path)},
        capture_output=True,
        text=True,
        check=False,
    )


def test_default_project(cookies):
    result = cookies.bake()

    assert result.exit_code == 0, result.exception
    assert result.project_path.name == "pylint-my-checks"
    checker = (result.project_path / "pylint_my_checks" / "my_check.py").read_text()
    assert "class MyCheckChecker(BaseChecker):" in checker
    assert '"W9901"' in checker
    assert (result.project_path / "tests" / "functional" / "my_check" / "my_check.py").is_file()
    unit = (result.project_path / "tests" / "test_my_check.py").read_text()
    assert "class TestMyCheckChecker(testutils.CheckerTestCase):" in unit
    assert (result.project_path / "LICENSE").read_text().startswith("MIT License")
    assert (result.project_path / ".git").is_dir()


def test_check_name_gives_module_and_class(cookies):
    result = cookies.bake(extra_context={"check_name": "z-combobulator"})

    assert result.exit_code == 0, result.exception
    checker = (result.project_path / "pylint_my_checks" / "z_combobulator.py").read_text()
    assert "class ZCombobulatorChecker(BaseChecker):" in checker
    assert '    def visit_while(self, node: nodes.While) -> None:' in checker
    init = (result.project_path / "pylint_my_checks" / "__init__.py").read_text()
    assert "linter.register_checker(ZCombobulatorChecker(linter))" in init


@pytest.mark.parametrize("license_name", ["MIT", "GPL-2.0-or-later"])
def test_generated_tests_pass(cookies, license_name):
    result = cookies.bake(
        extra_context={
            "plugin_name": "pylint-fruit-basket",
            "check_name": "no-rotten-apple",
            "message_id_prefix": "77",
            "license": license_name,
        }
    )

    assert result.exit_code == 0, result.exception
    tests = run_tests(result.project_path)
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert "3 passed" in tests.stdout


def test_example_raises_its_message(cookies):
    result = cookies.bake(extra_context={"check_name": "z-combobulator"})
    assert result.exit_code == 0, result.exception
    functional = result.project_path / "tests" / "functional" / "z_combobulator" / "z_combobulator.py"
    expected = functional.with_suffix(".txt")
    assert expected.read_text() == "z-combobulator:4:0:5:15::Used `while` loop:UNDEFINED\n"

    # Writing the expected output again does not change it.
    tests = run_functional_tests(result.project_path, "--update-functional-output")
    assert tests.returncode == 0, tests.stdout + tests.stderr
    assert expected.read_text() == "z-combobulator:4:0:5:15::Used `while` loop:UNDEFINED\n"

    # Without the annotation, the functional test fails and tells where.
    functional.write_text(functional.read_text().replace("  # [z-combobulator]", ""))
    tests = run_tests(result.project_path)
    assert tests.returncode == 1
    assert "4: z-combobulator (times 1)" in tests.stdout
    assert "1 failed, 2 passed" in tests.stdout


@pytest.mark.parametrize("prefix", ["12", "50", "100", "ab"])
def test_message_id_prefix_must_be_for_plugins(cookies, prefix):
    result = cookies.bake(extra_context={"message_id_prefix": prefix})

    assert result.exit_code != 0


@pytest.mark.parametrize("check_name", ["Z-combobulator", "my_check", "-z-combobulator", "apple2", "z"])
def test_check_name_must_be_a_symbol(cookies, check_name):
    result = cookies.bake(extra_context={"check_name": check_name})

    assert result.exit_code != 0


def test_module_name_must_be_valid(cookies):
    result = cookies.bake(extra_context={"module_name": "my-checks"})

    assert result.exit_code != 0
