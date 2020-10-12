from typing import List

import click


@click.command()
@click.argument("strings", nargs=-1)
def echo(strings: List[str]):
    r"""Echo the STRING(s) to standard output."""

    #    -n     do not output the trailing newline

    #    -e     enable interpretation of backslash escapes

    #    -E     disable interpretation of backslash escapes (default)

    #    --help display this help and exit

    #    --version
    #           output version information and exit

    #    If -e is in effect, the following sequences are recognized:

    #    \\     backslash

    #    \a     alert (BEL)

    #    \b     backspace

    #    \c     produce no further output

    #    \e     escape

    #    \f     form feed

    #    \n     new line

    #    \r     carriage return

    #    \t     horizontal tab

    #    \v     vertical tab

    #    \0NNN  byte with octal value NNN (1 to 3 digits)

    #    \xHH   byte with hexadecimal value HH (1 to 2 digits)
    # """
    ret = " ".join(strings)
    click.echo(ret)


def run():
    echo()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
