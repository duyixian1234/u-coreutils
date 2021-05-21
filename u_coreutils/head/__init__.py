import sys
from pathlib import Path
from typing import List

import click


def getLines(path: Path, n: int, reverse: bool = False):
    with path.open("r") as f:
        if reverse:
            return f.readlines()[-n:]
        return [f.readline() for _ in range(n)]


def getBytes(path: Path, n: int, reverse: bool = False):
    size = path.stat().st_size
    start = size - n if reverse else 0
    with path.open("r") as f:
        f.seek(start)
        return f.read(n)


@click.command()
@click.option(
    "-n",
    "--lines",
    type=int,
    help="print the first K bytes of each file; with the leading ' - ', print all but the last K bytes of each file",
)
@click.option(
    "-b",
    "--bytes",
    "_bytes",
    type=int,
    help=(
        "print the first K lines instead of the first 10; "
        "with the leading '-', print all but the last K lines of each file"
    ),
)
@click.option("-q", "--quiet", flag_value=True, help="never print headers giving file names")
@click.option("-v", "--verbose", flag_value=True, help="always print headers giving file names")
@click.argument("file", required=True, nargs=-1, type=click.Path(exists=True, readable=True))
def head(file: List[str], lines: int, _bytes: int, quiet: bool, verbose: bool):
    if lines and _bytes:
        click.echo("cannot specify both --bytes and --lines.")
        sys.exit(1)
    if not lines and not _bytes:
        lines = 10
    if len(file) > 1 and not quiet:
        verbose = True
    for _file in file:
        if verbose:
            click.echo(f">>>{_file}<<<")
        if lines:
            ret = "".join(getLines(Path(_file), abs(lines), lines < 0))
            click.echo(ret)
        else:
            ret = getBytes(Path(_file), abs(_bytes), _bytes < 0)
            click.echo(ret)


def run():
    head()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
