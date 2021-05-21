from click.testing import CliRunner

from u_coreutils.false import false


def test_false():
    runner = CliRunner()
    result = runner.invoke(false)
    assert result.exit_code == 1
