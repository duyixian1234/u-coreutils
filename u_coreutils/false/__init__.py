import sys

import click


@click.command()
def false():
    """do nothing, unsuccessfully"""
    sys.exit(1)


def run():
    false()
