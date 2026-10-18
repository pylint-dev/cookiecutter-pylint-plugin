"""Functional tests for {{ cookiecutter.check_name }}."""

apples = 0
while apples < 3:  # [{{ cookiecutter.check_name }}]
    apples += 1

for banana in range(3):
    print(banana)
