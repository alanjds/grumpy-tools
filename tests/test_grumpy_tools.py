#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `grumpy_tools` package."""
import os
import glob
import shutil
import tempfile

import pytest

from click.testing import CliRunner

from grumpy import cli


HERE = os.path.dirname(__file__)


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: ' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_run_input_inline(capfd):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['run', '-c', "print('Hello World')",])

    stdout_output, stderr_output = capfd.readouterr()
    assert stdout_output == 'Hello World\n'
    assert result.exit_code == 0


def test_run_input_stdin(capfd):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['run'], input="print('Hello World')")

    stdout_output, stderr_output = capfd.readouterr()
    assert stdout_output == 'Hello World\n'
    assert result.exit_code == 0


def test_run_input_file(capfd):
    runner = CliRunner()
    with tempfile.NamedTemporaryFile() as script_file:
        script_file.write("print('Hello World')")
        script_file.flush()

        result = runner.invoke(cli.main, ['run', script_file.name])

    stdout_output, stderr_output = capfd.readouterr()
    assert stdout_output == 'Hello World\n'
    assert result.exit_code == 0


def test_pep3147_transpile():
    runner = CliRunner()
    # Clear the folder to be created
    if os.path.exists('dummypackage/__pycache__'):
        shutil.rmtree('dummypackage/__pycache__')

    result = runner.invoke(cli.main, ['transpile', '--pep3147', HERE+'/dummypackage/ehlo.py'])

    assert result.exit_code == 0
    assert os.path.exists(HERE+'/dummypackage/__pycache__')
    assert glob.glob(HERE+'/dummypackage/__pycache__/*'), 'Nothing created on the __pycache__ folder'
    assert glob.glob(HERE+'/dummypackage/__pycache__/ehlo.grumpy*.pyc'), 'Wrong path created on the __pycache__ folder'
