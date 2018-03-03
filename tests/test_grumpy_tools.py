#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `grumpy_tools` package."""
import unittest

import pytest

from click.testing import CliRunner

from grumpy import cli


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


class GrumpyCLITest(unittest.TestCase):
    def setUp(self):
        self.cli = CliRunner()

    def test_run_input_inline(self):
        result = self.cli.invoke(cli.main, ['run', '--pep3147', '-c', "print('Hello World')",])
        # import wdb; wdb.set_trace()
        # assert result.output == 'Hello World'
        assert result.exit_code == 0
