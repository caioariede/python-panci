"""Utilities for converting from Travis CI configs to Tox configs."""

import six
import operator

from .travisconfig import TravisConfig
from .toxconfig import ToxConfig

from panci.utils import listify


def travis_env_to_tox_env(travis_python, travis_env):
    """Converts a Travis-style environment (e.g.: "2.6") to a Tox-style
    environment (e.g.: "py26")."""
    envlist = []

    for py in travis_python:
        if not isinstance(py, six.string_types):
            py = str(py)
        if not py.startswith('py') and py[1] == '.':
            py = 'py{ver}'.format(ver=py.replace('.', ''))
        if not travis_env:
            envlist.append((py, ''))
        else:
            for i, env in enumerate(travis_env):
                envname = '{py}-env{i}'.format(py=py, i=i+1)
                envlist.append((envname, env))

    return envlist


def travis2tox(in_file):
    """Takes a path or file object for a ``.travis.yml`` file and returns a
    ``ToxConfig`` object."""

    config = TravisConfig(in_file)

    py = listify(config.python)
    env = listify(getattr(config, 'env', []))

    envlist = travis_env_to_tox_env(py, env)

    commands = config.get_all_commands()

    return ToxConfig(envlist, commands)
