"""Provides a ``ToxConfig`` class for operating on ``tox.ini`` files"""

try:
    # Python 2
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser

from string import Template


class ToxConfig(object):
    """Class for operating on ``tox.ini`` files"""

    @classmethod
    def from_file(self, in_file):
        if not hasattr(in_file, 'read'):
            in_file = open(in_file, 'r')

        config_parser = ConfigParser()

        try:
            # Python 3
            config_parser.read_file(in_file)
        except AttributeError:
            # Python 2
            config_parser.readfp(in_file)

        return ToxConfig(
            envlist=list(map(str.strip, config_parser.get('tox', 'envlist').split(','))),
            commands=config_parser.get('testenv', 'commands')
        )


    def __init__(self, envlist, commands):
        """Create an object from a list of environments and a list of
        commands."""

        self.envlist = []
        self.setenv = []

        for envname, setenv in envlist:
            self.envlist.append(envname)
            if setenv:
                self.setenv.append((envname, setenv))

        self.commands = commands

    def getvalue(self):
        """Return a string with the contents of a ``tox.ini`` file."""

        envlist = ', '.join(self.envlist)

        setenv = self.get_setenv()
        commands = self.get_commands()

        items = []

        if setenv:
            items.append('setenv ={cmds}'.format(cmds=setenv))

        if commands:
            items.append('commands = {}'.format(commands))

        return Template("""
# Tox (http://tox.testrun.org/) is a tool for running tests
# in multiple virtualenvs. This configuration file will run the
# test suite on all supported python versions. To use it, "pip install tox"
# and then run "tox" from this directory.

[tox]
envlist = $envlist

[testenv]
$items
        """).substitute(
            envlist=envlist,
            items='\n'.join(items),
        ).lstrip()

    def get_setenv(self):
        """Return a string with the content of the ``setenv`` key for a
        ``tox.ini`` file."""

        setenv = []

        for env, vars_ in self.setenv:
            setenv.append('\n  - {env}: {vars}'.format(env=env, vars=vars_))

        return ''.join(setenv)

    def get_commands(self):
        """Return a string with the content of the ``commands`` key for a
        ``tox.ini`` file."""

        commands = []

        if hasattr(self.commands, 'startswith'):
            commands.append(self.commands)
        elif hasattr(self.commands, '__getitem__'):
            commands.extend(self.commands)

        if len(commands) == 1:
            return commands[0]
        elif len(commands) > 1:
            return "\n    " + "\n    ".join(commands)
