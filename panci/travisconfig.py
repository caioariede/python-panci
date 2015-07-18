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

    def get_install_commands(self):
        """Return a list of all install commands."""
        commands = []
        for key in ['before_install', 'install', 'after_install']:
            commands.extend(listify(getattr(self, key, [])))
        return commands

    def get_script_commands(self):
        """Return a list of all script commands."""
        commands = []
        for key in ['before_script', 'script', 'after_script']:
            commands.extend(listify(getattr(self, key, [])))
        return commands

    def get_apt_commands(self):
        """Return a list of all APT commands (e.g.: 'apt-get',
        'add-apt-repository')."""
        commands = []
        if hasattr(self, 'addons'):
            if 'apt' in self.addons:
                packages = self.addons['apt'].get('packages', [])
                for pkg in listify(packages):
                    commands.append(
                        'apt-get install {pkg}'.format(pkg=pkg))
                sources = self.addons['apt'].get('sources', [])
                for pkg in listify(sources):
                    commands.append(
                        'add-apt-repository ppa:{pkg}'.format(pkg=pkg))
        return commands

    def get_all_commands(self):
        """Return a list of all the commands in all of the fields that can
        contain commands (e.g.: 'before_install', 'install', 'after_install',
        'before_script', 'script', 'after_script')."""

        commands = []
        commands.extend(self.get_apt_commands())
        commands.extend(self.get_install_commands())
        commands.extend(self.get_script_commands())

        return commands

    def dumps(self):
        return yaml.dump(self.__dict__, default_flow_style=False, indent=2)
