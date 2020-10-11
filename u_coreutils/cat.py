from pathlib import Path
from typing import List

import click

LINE_NUMBER_WIDTH = 6


class LineFilter:
    def run(self, line: str, index: int = -1):
        raise NotImplementedError


class ShowEnds(LineFilter):
    def run(self, line: str, index: int = -1):
        return line.replace("\n", "$\n")


class ShowTabs(LineFilter):
    def run(self, line: str, index: int = -1):
        return line.replace("\t", "^I")


class ShowLineNumbers(LineFilter):
    def run(self, line: str, index: int = -1):
        return f"{index+1:{LINE_NUMBER_WIDTH}}  {line}"


class ShowNotBlankLineNumbers(LineFilter):
    lineIndex = 0

    def run(self, line: str, index: int = -1):
        if line != "\n":
            self.lineIndex += 1
            return f"{self.lineIndex:{LINE_NUMBER_WIDTH}}  {line}"
        else:
            return line


class SqueezeBlankLines(LineFilter):
    lastLine = ""

    def run(self, line: str, index: int = -1):

        if index == 0:
            self.lastLine = line

        if not self.lastLine and not line:
            return ""

        ret = self.lastLine
        self.lastLine = line
        return ret


COMBINE_OPTIONS = dict(showAllFlag=["showTabsFlag", "showEndFlag"])

PIPLINES = dict(
    showLineNumberFlag={1: ShowLineNumbers, 2: ShowNotBlankLineNumbers},
    showEndFlag={1: ShowEnds},
    showTabsFlag={1: ShowTabs},
    squeezeBlankFlag={1: SqueezeBlankLines},
)

PRIORITY = [
    ShowLineNumbers,
    ShowNotBlankLineNumbers,
    ShowTabs,
    SqueezeBlankLines,
    ShowEnds,
]


class Pipeline:
    def __init__(self, **kwargs):
        self.linePipeline = []

        for option in COMBINE_OPTIONS:
            if kwargs.get(option, None):
                kwargs.update({item: True for item in COMBINE_OPTIONS[option]})

        for k, v in kwargs.items():
            if v and issubclass(
                filterType := PIPLINES.get(k, {}).get(v, object), LineFilter
            ):
                self.linePipeline.append(filterType())

        self.linePipeline.sort(key=lambda x: PRIORITY.index(type(x)))

        def lineProcessor(line: str, index: int = -1):
            for filter in self.linePipeline:
                # click.secho(f"{filter=} {line=} {index=}", fg="green")
                line = filter.run(line, index)
            return line

        self.lineProcessor = lineProcessor

    def execute(self, line: str, index: int = -1):
        return self.lineProcessor(line, index)


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
@click.option(
    "-n", "--number", "showLineNumberFlag", flag_value=1, help="number all output lines"
)
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
    cat()


if __name__ == "__main__":
    run()
