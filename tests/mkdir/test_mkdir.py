from pathlib import Path

from click.testing import CliRunner

from u_coreutils.mkdir import mkdir


def test_mkdir():
    runner = CliRunner()
    with runner.isolated_filesystem():
        path = Path("a")
        path.mkdir()

        result = runner.invoke(mkdir, ["b"])
        assert result.exit_code == 0
        assert result.output == ""

        result = runner.invoke(mkdir, ["-v", "c"])
        assert result.exit_code == 0
        assert result.output == "mkdir: created directory 'c'\n"

        result = runner.invoke(mkdir, ["-v", "a"])
        assert result.exit_code == 1
        assert result.output == "mkdir: a: File exists\n"

        result = runner.invoke(mkdir, ["a/b"])
        assert result.exit_code == 0
        assert result.output == ""

        result = runner.invoke(mkdir, ["a/b/c/d"])
        assert result.exit_code == 1
        assert result.output == f"mkdir: {Path('a/b/c')}: No such file or directory\n"

        result = runner.invoke(mkdir, ["-p", "-v", "b/c/d"])
        assert result.exit_code == 0
        assert (
            result.output == f"mkdir: created directory '{Path('b/c')}'\nmkdir: created directory '{Path('b/c/d')}'\n"
        )
