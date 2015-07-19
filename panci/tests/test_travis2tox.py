import six
import unittest

from panci.travis2tox import travis2tox


class TravisToToxEnvsTests(unittest.TestCase):

    def test_no_env(self):
        travis = '''
language: python
python: 2.7
install:
  - echo 1
        '''

        tox_config = travis2tox(six.StringIO(travis))

        tox_file = tox_config.getvalue().splitlines()
        tox_file = '\n'.join(tox_file[5:])

        self.assertEqual(tox_file, '''[tox]
envlist = py27

[testenv]
commands = echo 1
        ''')

    def test_one_env(self):
        travis = '''
language: python
python:
  - 2.7
  - 3.4
env: DEPS=true
install:
  - echo 1
        '''

        tox_config = travis2tox(six.StringIO(travis))

        tox_file = tox_config.getvalue().splitlines()
        tox_file = '\n'.join(tox_file[5:])

        self.assertEqual(tox_file, '''[tox]
envlist = py27-env1, py34-env1

[testenv]
setenv =
  - py27-env1: DEPS=true
  - py34-env1: DEPS=true
commands = echo 1
        ''')

    def test_multiple_envs(self):
        travis = '''
language: python
python:
  - 2.7
  - 3.4
env:
  - DEPS=true
  - DEPS=false
install:
  - echo 1
        '''

        tox_config = travis2tox(six.StringIO(travis))

        tox_file = tox_config.getvalue().splitlines()
        tox_file = '\n'.join(tox_file[5:])

        self.assertEqual(tox_file, '''[tox]
envlist = py27-env1, py27-env2, py34-env1, py34-env2

[testenv]
setenv =
  - py27-env1: DEPS=true
  - py27-env2: DEPS=false
  - py34-env1: DEPS=true
  - py34-env2: DEPS=false
commands = echo 1
        ''')


class TravisToToxCommandsTests(unittest.TestCase):

    def test_before_install(self):
        travis = '''
language: python
python:
  - 2.7
before_install:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])

    def test_install(self):
        travis = '''
language: python
python:
  - 2.7
install:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])

    def test_after_install(self):
        travis = '''
language: python
python:
  - 2.7
after_install:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])

    def test_before_script(self):
        travis = '''
language: python
python:
  - 2.7
before_script:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])

    def test_script(self):
        travis = '''
language: python
python:
  - 2.7
script:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])

    def test_after_script(self):
        travis = '''
language: python
python:
  - 2.7
script:
  - echo 1
  - echo 2
        '''

        tox_config = travis2tox(six.StringIO(travis))
        self.assertEqual(tox_config.commands, ['echo 1', 'echo 2'])
