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
@click.option('-m', '--modname', help='Run the named module')
def transpile(args=None, script=None, modname=None):
    import sys
    sys.argv.pop(0)
    return grumpc.main(grumpc.parser.parse_args())


@main.command('run')
@click.option('-m', '--modname', help='Run the named module')
def transpile(modname=None):
    import sys
    sys.argv.pop(0)
    return grumprun.main(modname=modname)


if __name__ == "__main__":
    import sys
    sys.exit(main())
