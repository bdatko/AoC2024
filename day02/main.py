from collections.abc import Iterator, Sequence
from enum import Enum
from itertools import pairwise
from pathlib import Path

import click


class Sign(Enum):
    START = "START"
    DECREASING = "DECREASING"
    INCREASING = "INCREASING"


def get_rows(infile: Path, *, delimiter: str) -> Iterator[list[int]]:
    with infile.open(mode="r", encoding="utf-8") as file:
        for line in file:
            yield [int(value.strip()) for value in line.split(delimiter)]


def diff(rows: Iterator[Sequence[int]]) -> Iterator[list[int]]:
    for row in rows:
        yield [right - left for left, right in pairwise(row)]


def safe(rows: Iterator[list[int]]) -> Iterator[bool]:
    for row in rows:
        safe_report = True
        sign = Sign.START
        for diff in row:
            if not safe_report:
                break
            if abs(diff) > 3 or diff == 0:
                safe_report = False
                continue
            match sign:
                case Sign.START if diff < 0:
                    sign = Sign.DECREASING
                case Sign.START if diff > 0:
                    sign = Sign.INCREASING
                case Sign.INCREASING if diff < 0:
                    safe_report = False
                    continue
                case Sign.DECREASING if diff > 0:
                    safe_report = False
                    continue
        yield safe_report


@click.group()
def cli():
    pass


@click.command(short_help="Solution to part 01")
@click.argument(
    "infile",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        path_type=Path,
    ),
)
@click.option(
    "--delimiter",
    type=click.STRING,
    help="The delimiter seperating the columns within [INFILE]",
)
def first(infile: Path, delimiter: str) -> None:
    rows = get_rows(infile, delimiter=delimiter)

    rows = diff(rows)

    rows = safe(rows)

    result = sum(result for result in rows)
    click.echo(result)


@click.command(short_help="Solution to part 02")
@click.argument(
    "infile",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        path_type=Path,
    ),
)
@click.option(
    "--delimiter",
    type=click.STRING,
    help="The delimiter seperating the columns within [INFILE]",
)
def second(infile: Path, delimiter: str) -> None:
    pass


cli.add_command(first)
if __name__ == "__main__":
    cli()
