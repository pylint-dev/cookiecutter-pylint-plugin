"""Unit tests for {{ cookiecutter.check_name }}, with pylint's ``CheckerTestCase``.

A unit test runs one checker on a piece of code parsed by astroid.

Upsides:

- It is fast: nothing else of pylint runs.
- It is easy to follow in a debugger, from the test to your ``visit_`` method.

Downsides:

- You write each expected message by hand, with its node and position.
- Only your checker runs: not the other checkers, not the configuration,
  not the ``register`` function of the plugin. A test can pass while the
  plugin does not work in pylint.
- Messages from other checkers are not seen, so you will not notice a
  conflict with them.

The functional tests in ``test_functional.py`` are closer to what your users
get. Use unit tests for small cases you want to check quickly.
"""

from __future__ import annotations

import astroid
from pylint import testutils

from {{ cookiecutter.module_name }}.{{ cookiecutter.__checker_module }} import {{ cookiecutter.__checker_class }}


class Test{{ cookiecutter.__checker_class }}(testutils.CheckerTestCase):
    """Run {{ cookiecutter.__checker_class }} alone on small pieces of code."""

    CHECKER_CLASS = {{ cookiecutter.__checker_class }}

    def test_for_loop_is_fine(self) -> None:
        """A ``for`` loop is not a ``while`` loop."""
        module = astroid.parse(
            """
            for apple in range(3):
                print(apple)
            """
        )
        with self.assertNoMessages():
            self.walk(module)

    def test_while_loop(self) -> None:
        """Each ``while`` loop gets a message."""
        # ``#@`` marks the node that extract_node returns.
        while_node = astroid.extract_node(
            """
            apples = 0
            while apples < 3:  #@
                apples += 1
            """
        )
        with self.assertAddsMessages(
            testutils.MessageTest(
                "{{ cookiecutter.check_name }}",
                node=while_node,
                line=3,
                col_offset=0,
                end_line=4,
                end_col_offset=15,
            )
        ):
            self.walk(while_node.root())
