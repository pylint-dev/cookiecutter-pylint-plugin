# cookiecutter-pylint-plugin

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template to start a
[pylint](https://github.com/pylint-dev/pylint) plugin.

The new project comes with:

- your first checker, named after your check: answer `z-combobulator` and you get a
  `ZCombobulatorChecker` that raises a `z-combobulator` message on each `while` loop,
  an example to replace with your own check,
- functional tests: a Python file shows where pylint should warn, and a `.txt` file
  holds the expected output,
- a unit test with pylint's `CheckerTestCase`, faster but running the checker alone,
- a `pyproject.toml` ready to publish on PyPI,
- a GitHub Actions workflow that runs the tests,
- a pre-commit configuration with ruff.

## Use

```bash
pipx run cookiecutter gh:pylint-dev/cookiecutter-pylint-plugin
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uvx cookiecutter gh:pylint-dev/cookiecutter-pylint-plugin
```

You will be asked for:

| Question | Default | What it is |
|----------|---------|------------|
| `full_name`, `email` | | The author of the plugin. |
| `github_username` | | Used in the link to the source code. |
| `plugin_name` | `pylint-my-checks` | The name on PyPI. |
| `module_name` | `pylint_my_checks` | The Python package, the one given to `--load-plugins`. |
| `check_name` | `my-check` | Your first check. It is the symbol of its message, and gives the names of the checker module and class. Lower case letters and `-` only. |
| `short_description` | | One sentence about the plugin. |
| `message_id_prefix` | `99` | Two digits between 51 and 99, [the range pylint keeps for plugins](https://pylint.readthedocs.io/en/latest/development_guide/how_tos/custom_checkers.html). Your messages will be `W9901`, `W9902`, ... Pick a number that other plugins you use do not have. |
| `license` | `MIT` | `MIT` or `GPL-2.0-or-later`, the license of pylint. |

Then follow the README of the new project.

## Develop the template

```bash
pip install --group test
pytest
```

The tests generate projects from the template and run their tests.
