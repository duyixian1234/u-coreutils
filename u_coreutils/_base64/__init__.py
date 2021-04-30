import base64
import sys
from pathlib import Path

import click


def fromInput() -> bytes:
    content = b""
    while True:
        try:
            content += input().encode()
        except EOFError:
            return content


def fromFile(file: str) -> bytes:
    path = Path(file)
    if not path.exists():
        click.echo(f"u-base64: {file}: No such file or directory")
        sys.exit(1)
    if not path.is_file():
        click.echo("u-base64: Read Error: It's directory")
        sys.exit(1)
    return path.read_bytes()


def getContent(file: str) -> bytes:
    if file == "-":
        return fromInput()
    return fromFile(file)


def transfer(content: bytes, decode: bool) -> bytes:
    if decode:
        return base64.b64decode(content)
    return base64.b64encode(content)


def display(output: bytes, decode: bool, wrap: int):
    if decode or not wrap:
        print(output.decode())
        return
    while output:
        print(output[:wrap].decode())
        output = output[wrap:]


@click.command()
@click.option("-d", "--decode", is_flag=True, help="Decode data")
@click.option(
    "-w",
    "--wrap",
    type=int,
    default=76,
    help="Wrap encoded lines after COLS character (default 76). Use 0 to disable line wrapping.",
)
@click.argument("file", required=True)
def _base64(file: str, wrap: int, decode: bool):
    """Base64 encode or decode FILE, or standard input, to standard output.
    With no FILE, or when FILE is -, read standard input."""
    content = getContent(file)
    output = transfer(content, decode=decode)
    display(output, decode=decode, wrap=wrap)


def run():
    _base64()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
