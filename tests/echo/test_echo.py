from click.testing import CliRunner
from u_coreutils.echo import echo, getChar, escape, parseCode


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

        result = runner.invoke(echo, ["-e", r"\0111NG"])
        assert result.exit_code == 0
        assert result.output == "ING\n"

        result = runner.invoke(echo, ["-e", r"\x49NG"])
        assert result.exit_code == 0
        assert result.output == "ING\n"


def testGetChar():
    data = dict(value="a")
    assert getChar(data) == "a"
    assert getChar(data) == ""


def testEscape():
    assert escape("abc\\n\\t\\\\") == "abc\n\t\\"
    assert escape("abc\cdef") == "abc"


def testParseCode():
    data = dict(value="111abc")
    assert parseCode(data, 8, 3, 3) == "I"
    assert data["value"] == "abc"

    data["value"] = "77abc"
    assert parseCode(data, 8, 3, 3) == "?"
    assert data["value"] == "abc"

    data["value"] = "49abc"
    assert parseCode(data, 16, 2, 4) == "I"
    assert data["value"] == "abc"

    data["value"] = "1"
    assert parseCode(data, 8, 3, 3) == "\x01"
