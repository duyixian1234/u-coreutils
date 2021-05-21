from click.testing import CliRunner

from u_coreutils.factor import _factor, factor, gen_primes


def test_factor():
    assert list(factor(10, [], gen_primes())) == [2, 5]


def test_cli():
    runner = CliRunner()
    result = runner.invoke(_factor, "10")
    assert result.exit_code == 0
    assert result.output == "10: 2 5\n"
