"""The {{ cookiecutter.check_name }} checker."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages


class {{ cookiecutter.__checker_class }}(BaseChecker):
    """Warn on each ``while`` loop.

    This is an example: replace it, the message and the tests with your own check.
    """

    name = "{{ cookiecutter.check_name }}"
    msgs = {
        # W is the category (Warning), {{ cookiecutter.message_id_prefix }} is the id of this
        # plugin, 01 is the number of the message inside the plugin.
        "W{{ cookiecutter.message_id_prefix }}01": (
            "Used `while` loop",
            "{{ cookiecutter.check_name }}",
            "Unbounded `while` loops can often be rewritten as bounded `for` loops.",
        )
    }

    # pylint calls visit_<node type> for each node of that type it finds, and
    # leave_<node type> once it is done with the node and everything inside it.
    # The node types are the classes in astroid.nodes, in lower case.
    @only_required_for_messages("{{ cookiecutter.check_name }}")
    def visit_while(self, node: nodes.While) -> None:
        """Called for each ``while`` loop in the code."""
        self.add_message("{{ cookiecutter.check_name }}", node=node)
