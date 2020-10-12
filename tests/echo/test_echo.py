from click.testing import CliRunner
from u_coreutils.echo import echo, getChar, escape


def test_echo():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(echo, ["a", "b", "c"])
        assert result.exit_code == 0
        assert result.output == "a b c\n"

        result = runner.invoke(echo, ["-n", "hello"])
        assert result.exit_code == 0
        assert result.output == "hello"

        result = runner.invoke(echo, ["-e", r"a\n\t"])
        assert result.exit_code == 0
        assert result.output == "a\n\t\n"


def testGetChar():
    data = dict(value="a")
    assert getChar(data) == "a"
    assert getChar(data) == ""


def testEscape():
    assert escape("abc\\n\\t\\\\") == "abc\n\t\\"
    assert escape("abc\cdef") == "abc"
