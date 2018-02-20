# -*- coding: utf-8 -*-

"""Console script for grumpy_tools."""

import click

from . import grumpc, grumprun


@click.group('grumpy')
def main(args=None):
    """Console script for grumpy_tools."""
    return 0

@main.command('transpile')
@click.argument('script')
@click.option('-m', '--modname', default='__main__', help='Run the named module')
def transpile(script=None, modname=None):
    return grumpc.main(script=script, modname=modname)


@main.command('run')
@click.option('-m', '--modname', help='Run the named module')
def transpile(modname=None):
    return grumprun.main(modname=modname)


if __name__ == "__main__":
    import sys
    sys.exit(main())
