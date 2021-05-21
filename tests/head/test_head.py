from click.testing import CliRunner

from u_coreutils.head import head


def test_head():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("data.txt", "w") as f:
            f.writelines(["*" * n + "\n" for n in range(1, 12)])

        with open("data1.txt", "w") as f:
            f.write("Hello,World")

        result = runner.invoke(head, ["data.txt"])
        assert result.exit_code == 0
        expect = "".join(["*" * n + "\n" for n in range(1, 11)])
        assert result.output == expect + "\n"

        result = runner.invoke(head, ["-n 5", "data.txt"])
        assert result.exit_code == 0
        expect = "".join(["*" * n + "\n" for n in range(1, 6)])
        assert result.output == expect + "\n"

        result = runner.invoke(head, ["-n -5", "data.txt"])
        assert result.exit_code == 0
        expect = "".join(["*" * n + "\n" for n in range(7, 12)])
        assert result.output == expect + "\n"

        result = runner.invoke(head, ["-b 5", "data1.txt"])
        assert result.exit_code == 0
        assert result.output == "Hello\n"

        result = runner.invoke(head, ["-b -5", "data1.txt"])
        assert result.exit_code == 0
        assert result.output == "World\n"

        result = runner.invoke(head, ["-b -5", "-n 5", "data1.txt"])
        assert result.exit_code == 1

        result = runner.invoke(head, ["data.txt", "data1.txt"])
        assert result.exit_code == 0
        expect = (
            ">>>data.txt<<<\n"
            + "".join(["*" * n + "\n" for n in range(1, 11)])
            + "\n"
            + ">>>data1.txt<<<\n"
            + "Hello,World\n"
        )
        assert result.output == expect

        result = runner.invoke(head, ["-q", "data.txt", "data1.txt"])
        assert result.exit_code == 0
        expect = "".join(["*" * n + "\n" for n in range(1, 11)]) + "\n" + "Hello,World\n"
        assert result.output == expect

        result = runner.invoke(head, ["-v", "data1.txt"])
        assert result.exit_code == 0
        assert result.output == ">>>data1.txt<<<\nHello,World\n"
