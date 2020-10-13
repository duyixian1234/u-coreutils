from typing import List

import click

# pylint: disable=anomalous-backslash-in-string
ESCAPES = {"a": "\a", "b": "\b", "e": "\e", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v", "\\": "\\"}
CODES = {"0": (8, 3, 3), "x": (16, 2, 4)}


def getChar(data: dict):
    if not data["value"]:
        return ""
    ret = data["value"][0]
    data["value"] = data["value"][1:]
    return ret


def addChar(data: dict, char: str):
    data["value"] = char + data["value"]


def parseCode(data: dict, base: int, maxDigits: int, bitsPerDigit: int):
    ret = 0
    for _ in range(maxDigits):
        if char := getChar(data):
            try:
                digit = int(char, base)
                ret = (ret << bitsPerDigit) | digit
            except ValueError:
                addChar(data, char)
                break
        else:
            break
    return chr(ret)


def escape(string: str):
    data = {"value": string}
    ret = []
    while char := getChar(data):
        if char == "\\" and data["value"]:
            char = getChar(data)
            if char in ESCAPES:
                ret.append(ESCAPES[char])
            if char in CODES:
                ret.append(parseCode(data, *CODES[char]))
            elif char == "c":
                break
        else:
            ret.append(char)
    return "".join(ret)


@click.command()
@click.option("-n", "noNewLineFlag", flag_value=True, help="do not output the trailing newline")
@click.option("-e", "escapeFlag", flag_value=True, help="enable interpretation of backslash escapes", default=False)
@click.option("-E", "escapeFlag", flag_value=False, help="disable interpretation of backslash escapes (default)")
@click.argument("strings", nargs=-1)
def echo(strings: List[str], escapeFlag: bool, noNewLineFlag: bool):
    r"""Echo the STRING(s) to standard output.

    If -e is in effect, the following sequences are recognized:

    \\     backslash

    \a     alert (BEL)

    \b     backspace

    \c     produce no further output

    \e     escape

    \f     form feed

    \n     new line

    \r     carriage return

    \t     horizontal tab

    \v     vertical tab

    \0NNN  byte with octal value NNN (1 to 3 digits)

    \xHH   byte with hexadecimal value HH (1 to 2 digits)
    """
    if escapeFlag:
        strings = [escape(string) for string in strings]
    ret = " ".join(strings)
    click.echo(ret, nl=not noNewLineFlag)


def run():
    echo()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
