from click.testing import CliRunner

from u_coreutils.cat import cat


def test_cat():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("Hello World!")

        with open("hello1.txt", "w") as f:
            f.write("Hello\tWorld!\nHello world!")

        result = runner.invoke(cat, ["hello.txt"])
        assert result.exit_code == 0
        assert result.output == "Hello World!"

        result = runner.invoke(cat, ["-A", "-n", "hello.txt", "hello1.txt"])
        assert result.exit_code == 0
        assert result.output == "     1  Hello World!Hello^IWorld!$\n     2  Hello world!"
