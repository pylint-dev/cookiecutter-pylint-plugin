# {{ cookiecutter.plugin_name }}

{{ cookiecutter.short_description }}

## Install

```bash
pip install {{ cookiecutter.plugin_name }}
```

## Use

Load the plugin when you run pylint:

```bash
pylint --load-plugins={{ cookiecutter.module_name }} my_code.py
```

Or add it to your `pyproject.toml`, so it is loaded every time:

```toml
[tool.pylint.main]
load-plugins = ["{{ cookiecutter.module_name }}"]
```

## Messages

- `W{{ cookiecutter.message_id_prefix }}01` (`{{ cookiecutter.check_name }}`): a `while` loop is used. This is an example to
  replace with your own check.

## Develop

The version comes from git tags, with
[setuptools-scm](https://setuptools-scm.readthedocs.io/): tag a commit `v0.1.0` to release `0.1.0`.

Install the plugin with its test dependencies (pip 25.1 or newer), then run the tests:

```bash
pip install -e . --group test
pytest
```

### Add a check

1. Write a checker in `{{ cookiecutter.module_name }}/`, using `{{ cookiecutter.__checker_module }}.py` as a model.
   Give each new message the next free id, `W{{ cookiecutter.message_id_prefix }}02` for example.
2. Register it in the `register` function of `{{ cookiecutter.module_name }}/__init__.py`.
3. Add a test file in `tests/functional/`. Put `# [message-symbol]` at the end
   of each line where pylint should warn.
4. Write the expected output next to it:

   ```bash
   python tests/test_functional.py --update-functional-output
   ```

   This creates a `.txt` file with the same name. Read it to check that the messages are right.

A test file can have a `.rc` file with the same name to give pylint some options, for example:

```ini
[MAIN]
max-line-length=120
```
