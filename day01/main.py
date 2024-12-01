from bisect import insort
from collections import Counter, defaultdict
from collections.abc import Iterator, Sequence
from itertools import pairwise
from pathlib import Path

import click

infile = Path("input")


def get_rows(
    infile: Path, *, delimiter: str, field_names: Sequence[str]
) -> Iterator[dict[str, int]]:
    with infile.open(mode="r", encoding="utf-8") as file:
        for line in file:
            split = (int(value.strip()) for value in line.split(delimiter))
            yield dict(zip(field_names, split))


def sorting(
    rows: Iterator[dict[str, int]], field_names: Sequence[str]
) -> Iterator[tuple[int, int]]:

    store = defaultdict(list)
    for row in rows:
        for name in field_names:
            insort(store[name], row[name])

    yield from zip(*(store[name] for name in field_names))


def symm(rows: Iterator[dict[str, int]], field_names: Sequence[str]) -> Iterator[int]:

    store = defaultdict(Counter)
    for row in rows:
        for name in field_names:
            store[name][row[name]] += 1

    for left, right in pairwise(field_names):
        count_left, count_right = store[left], store[right]
        for item in count_left:
            symmetry = 0
            if item in count_right:
                symmetry = item * count_right[item]
            yield symmetry


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
@click.option(
    "--field-names",
    type=click.STRING,
    multiple=True,
    help="The name of the fields. Pass multiple fields with multiple options.",
)
def first(infile: Path, delimiter: str, field_names: Sequence[str]) -> None:
    rows = get_rows(infile, delimiter=delimiter, field_names=field_names)

    rows = sorting(rows, field_names=field_names)

    result = sum(abs(left - right) for left, right in rows)
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
@click.option(
    "--field-names",
    type=click.STRING,
    multiple=True,
    help="The name of the fields. Pass multiple fields with multiple options.",
)
def second(infile: Path, delimiter: str, field_names: Sequence[str]) -> None:
    rows = get_rows(infile, delimiter=delimiter, field_names=field_names)
    rows = symm(rows, field_names=field_names)
    result = sum(rows)
    click.echo(result)


cli.add_command(first)
cli.add_command(second)
if __name__ == "__main__":
    cli()
