"""Provides a ``TravisConfig`` class for operating on ``.travis.yml`` files"""

import yaml

from panci.utils import listify


class TravisConfig(object):
    """Class for operating on ``.travis.yml`` files"""

    def __init__(self, in_file=None):
        """Create an object from a file object or filename referencing a
        ``.travis.yml`` file."""

        if in_file:
            if not hasattr(in_file, 'read'):
                in_file = open(in_file, 'r')

            self.__dict__ = yaml.load(in_file)

    def get_all_commands(self):
        """Return a list of all the commands in all of the fields that can
        contain commands (e.g.: 'before_install', 'install', 'after_install',
        'before_script', 'script', 'after_script')."""

        commands = []

        for key in ['before_install', 'install', 'after_install',
                    'before_script', 'script', 'after_script']:
            commands.extend(listify(getattr(self, key, [])))

        return commands

    def dumps(self):
        return yaml.dump(self.__dict__, default_flow_style=False, indent=2)
