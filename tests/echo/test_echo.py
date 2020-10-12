from click.testing import CliRunner
from u_coreutils.echo import echo


def test_echo():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(echo, ["a", "b", "c"])
        assert result.exit_code == 0
        assert result.output == "a b c\n"