# -*- coding: utf-8 -*-

"""Console script for grumpy_tools."""
import sys
from StringIO import StringIO

import click
from click_default_group import DefaultGroup

from . import grumpc, grumprun


@click.group('grumpy', cls=DefaultGroup, default='run', default_if_no_args=True)
def main(args=None):
    """
    Console script for grumpy_tools.

    The default command `grumpy run` will ran if no other selected.
    It mimics the CPython options, when possible and applicable.
    Please take a look on `grumpy run --help` for its implemented options.

    Example: all the following lines outputs Hello on the STDOUT\n
        $ python -c 'print("Hello")'\n
        $ grumpy -c 'print("Hello")'\n
        $ grumpy run -c 'print("Hello")'
    """
    return


@main.command('transpile')
@click.argument('script')
@click.option('-m', '--modname', default='__main__', help='Python module name')
@click.option('--pep3147', is_flag=True, help='Put the transpiled outputs on a __pycache__ folder')
def transpile(script=None, modname=None, pep3147=False):
    """
    Translates the python SCRIPT file to Go, then prints to stdout
    """
    try:
        output = grumpc.main(script=script, modname=modname, pep3147=pep3147)
    except RuntimeError as e:
        print >> sys.stderr, e.message
        sys.exit(e.exitcode)

    ## sys.stdout.write is harder to be tested.
    click.echo(output)
    sys.exit(0)


@main.command('run')
@click.argument('file', required=False, type=click.File('rb'))
@click.option('-c', '--cmd', help='Program passed in as string')
@click.option('-m', '--modname', help='Run run library module as a script')
@click.option('--pep3147', is_flag=True, help='Put the transpiled outputs on a __pycache__ folder')
def run(file=None, cmd=None, modname=None, pep3147=False):
    if modname:
        stream = None
    elif file:
        stream = StringIO(file.read())
    elif cmd:
        stream = StringIO(cmd)
    else:   # Read from STDIN
        stream = StringIO(click.get_text_stream('stdin').read())

    if stream is not None:
        stream.seek(0)

    result = grumprun.main(stream=stream, modname=modname, pep3147=pep3147)
    sys.exit(result)


if __name__ == "__main__":
    import sys
    sys.exit(main())
