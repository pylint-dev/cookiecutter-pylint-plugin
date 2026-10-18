"""{{ cookiecutter.short_description }}"""

from __future__ import annotations

from typing import TYPE_CHECKING

from {{ cookiecutter.module_name }}.{{ cookiecutter.__checker_module }} import {{ cookiecutter.__checker_class }}

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: PyLinter) -> None:
    """Called by pylint when the plugin is loaded with --load-plugins."""
    linter.register_checker({{ cookiecutter.__checker_class }}(linter))
