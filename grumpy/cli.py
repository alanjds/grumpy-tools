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
def transpile(args=None, script=None):
    import sys
    sys.argv.pop(0)
    return grumpc.main(grumpc.parser.parse_args())


@main.command('run')
@click.option('-m', '--modname', help='Run the named module')
def transpile(args=None, modname=None):
    import sys
    sys.argv.pop(0)
    return grumprun.main(grumprun.parser.parse_args())


if __name__ == "__main__":
    import sys
    sys.exit(main())
