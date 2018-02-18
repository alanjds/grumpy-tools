# -*- coding: utf-8 -*-

"""Console script for grumpy_tools."""

import click

import grumpc


@click.group('grumpy')
def main(args=None):
    """Console script for grumpy_tools."""
    click.echo("Replace this message by putting your code into "
               "grumpy_tools.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0

@main.command('transpile')
@click.argument('script')
def transpile(args=None, script=None):
    import sys
    sys.argv.pop(0)
    return grumpc.main(grumpc.parser.parse_args())


if __name__ == "__main__":
    import sys
    sys.exit(main())
