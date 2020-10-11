from pathlib import Path

import click

from .pipeline import Pipeline


@click.command()
@click.option(
    "-A",
    "--show-All",
    "showAllFlag",
    flag_value=1,
    help="Equivalent to -ET",
)
@click.option(
    "-b",
    "--number-nonblank",
    "showLineNumberFlag",
    flag_value=2,
    help="number nonempty output lines, overrides -n",
)
@click.option(
    "-E",
    "--show-ends",
    "showEndFlag",
    flag_value=True,
    help="display $ at end of each line",
)
@click.option("-n", "--number", "showLineNumberFlag", flag_value=1, help="number all output lines")
@click.option(
    "-s",
    "--squeeze-blank",
    "squeezeBlankFlag",
    flag_value=1,
    help="Suppress repeated empty output lines",
)
@click.option(
    "-T",
    "--show-tabs",
    "showTabsFlag",
    flag_value=True,
    help="Display TAB characters as ^I",
)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def cat(files, **kwargs):
    """concatenate files and print on the standard output"""
    pipeline = Pipeline(**kwargs)
    index = 0
    lastLine = ""
    for file in files:
        with Path(file).open() as f:
            while line := f.readline():
                if not lastLine.endswith("\n"):
                    lastLine += line
                else:
                    result = pipeline.execute(lastLine, index)
                    click.echo(result, nl=False)
                    lastLine = line
                    index += 1
    result = pipeline.execute(lastLine, index)
    click.echo(result, nl=False)


def run():
    cat()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
