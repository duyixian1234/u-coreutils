from pathlib import Path
from click.testing import CliRunner
from u_coreutils._base64 import _base64


def test_base64():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("temp.txt", "w") as f:
            f.write("abc")

        result = runner.invoke(_base64, ["temp.txt"])
        assert result.exit_code == 0
        assert result.output == "YWJj\n"

        result = runner.invoke(_base64, ["temp1.txt"])
        assert result.exit_code == 1
        assert result.output == "u-base64: temp1.txt: No such file or directory\n"

        Path("temp").mkdir()
        result = runner.invoke(_base64, ["temp"])
        assert result.exit_code == 1
        assert result.output == "u-base64: Read Error: It's directory\n"

        result = runner.invoke(_base64, ["-"], input="abc")
        assert result.exit_code == 0
        assert result.output == "YWJj\n"

        result = runner.invoke(_base64, ["-d", "-"], input="YWJj")
        assert result.exit_code == 0
        assert result.output == "abc\n"
