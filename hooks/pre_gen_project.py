"""Check the answers before the project is generated."""

import re
import sys

MODULE_NAME = "{{ cookiecutter.module_name }}"
CHECK_NAME = "{{ cookiecutter.check_name }}"
MESSAGE_ID_PREFIX = "{{ cookiecutter.message_id_prefix }}"

if not re.fullmatch(r"[a-z_][a-z0-9_]*", MODULE_NAME):
    sys.exit(f"'{MODULE_NAME}' is not a valid Python package name.")

# The check name is the message symbol, and gives the module and class names.
# Functional tests only find symbols made of lower case letters and "-".
if not re.fullmatch(r"[a-z]+(-[a-z]+)*", CHECK_NAME) or len(CHECK_NAME) < 2:
    sys.exit(f"'{CHECK_NAME}' must be lower case words joined by '-', without digits, like 'no-rotten-apple'.")

# 51-99 is reserved for plugins, see
# https://pylint.readthedocs.io/en/latest/development_guide/how_tos/custom_checkers.html
if not re.fullmatch(r"\d\d", MESSAGE_ID_PREFIX) or not 51 <= int(MESSAGE_ID_PREFIX) <= 99:
    sys.exit(f"The message id prefix must be between 51 and 99, not '{MESSAGE_ID_PREFIX}'.")
