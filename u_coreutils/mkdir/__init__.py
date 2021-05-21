import sys
from pathlib import Path
from typing import List

import click


def process(directory: str, mode: int = 0o755, parents: bool = False, verbose: bool = False):
    path = Path(directory)
    existsList = reversed([(_path.exists(), _path) for _path in list(path.parents)[:-1]])

    if path.exists() and not parents:
        click.echo(f"mkdir: {directory}: File exists")
        sys.exit(1)

    for exists, parentPath in existsList:
        if not exists:
            if parents:
                parentPath.mkdir(mode)
                if verbose:
                    click.echo(f"mkdir: created directory '{parentPath}'")
            else:
                click.echo(f"mkdir: {parentPath}: No such file or directory")
                sys.exit(1)

    path.mkdir(mode)
    if verbose:
        click.echo(f"mkdir: created directory '{path}'")


@click.command()
@click.option("-m", "--mode", help="set file mode (as in chmod), not a=rwx - umask", default="755")
@click.option(
    "-p",
    "--parents",
    flag_value=True,
    help="no error if existing, make parent directories as needed",
)
@click.option("-v", "--verbose", flag_value=True, help="print a message for each created directory")
@click.argument("DIRECTORY", required=True, nargs=-1, type=str)
def mkdir(directory: List[str], mode: str, parents: bool, verbose: bool):
    """Create the DIRECTORY(ies), if they do not already exist."""
    _mode = int(mode, 8)
    for _directory in directory:
        process(_directory, _mode, parents, verbose)


def run():
    mkdir()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
