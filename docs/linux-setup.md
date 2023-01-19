# Linux dev environment steps

## Prerequisites

### Install system dependencies

- [poetry](https://python-poetry.org/docs/#installation)
- [pyenv](https://github.com/pyenv/pyenv)
  - and [its dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
  - verify installation with `pyenv doctor` 

### Setup pyenv for project

1. `pyenv virtualenv 3.10 hitfactorpy`: create a virtualenv named "hitfactorpy" using python v3.10
2. `pyenv local hitfactorpy`: configure pyenv to use "hitfactorpy" for the current directory
3. `pyenv activate hitfactorpy`: activate the virtualenv

### Configure poetry to recognize pyenv

1. `poetry config virtualenvs.prefer-active-python true`
2. Verify output of `poetry env info`; the paths for `Virtualenv` and `System` should match the value of `$PYENV_ROOT` (default: `$HOME/.pyenv`)

## Development

1. Install dependencies: `poetry install`
2. Test: `poetry run tox`
3. Build: `poetry build`
