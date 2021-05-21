from typing import Generator, List

import click


def gen_primes():
    n = 2
    primes = []
    while True:
        if all(n % x for x in primes):
            yield n
            primes.append(n)
        n += 1


def factor(n: int, primes: List[int], generator: Generator[int, None, None]):
    start = prepare(n, primes, generator)

    for prime in primes[start:]:
        if n % prime == 0:
            yield prime
            yield from factor(n // prime, primes, generator)
            return


def prepare(n: int, primes: List[int], generator: Generator[int, None, None]):
    start = 0
    find = False
    while not primes or primes[-1] < n:
        index = len(primes)
        prime = next(generator)
        primes.append(prime)
        if not find and n % prime == 0:
            start = index
            find = True
    return start


@click.command()
@click.argument("number", required=True, type=int)
def _factor(number: int):
    """Print  the  prime  factors  of each specified integer NUMBER.  If none are specified on the command line, read
    them from standard input."""
    factors = list(factor(number, [], gen_primes()))
    click.echo(f'{number}: {" ".join(str(num) for num in factors)}')


def run():
    _factor()  # pylint: disable=no-value-for-parameter


__all__ = ["run"]
