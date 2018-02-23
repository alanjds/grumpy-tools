# -*- coding: utf-8 -*-

"""Console script for grumpy_tools."""
import sys

import click

from . import grumpc, grumprun


@click.group('grumpy')
def main(args=None):
    """Console script for grumpy_tools."""
    return 0


@main.command('transpile')
@click.argument('script')
@click.option('-m', '--modname', default='__main__', help='Python module name')
@click.option('--pep3147', is_flag=True, help='Put the transpiled outputs on a __pycache__ folder')
def transpile(script=None, modname=None, pep3147=False):
    """
    Translates the python SCRIPT file to Go, then prints to stdout
    """
    result = grumpc.main(script=script, modname=modname, pep3147=pep3147)
    sys.exit(result)


@main.command('run')
@click.option('-m', '--modname', help='Run the named module')
def run(modname=None):
    result = grumprun.main(modname=modname)
    sys.exit(result)


if __name__ == "__main__":
    import sys
    sys.exit(main())
