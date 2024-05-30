import json
from pathlib import Path

import click

from mids.cli_utils import print_check, print_report, get_gbif_data, get_data_from_url


@click.group("mids")
def cli():
    pass


@cli.command("report-url")
@click.argument("url", type=click.STRING)
@click.option("-v", "--verbose", is_flag=True, default=False)
def report_url(url: str, verbose: bool = False):
    data = get_data_from_url(url)
    print_report(data, verbose=verbose)


@cli.command("report-file")
@click.argument("file", type=click.File())
@click.option("-v", "--verbose", is_flag=True, default=False)
def report_file(path: Path, verbose: bool = False):
    with path.open() as f:
        print_report(json.load(f), verbose=verbose)


@cli.command("report-gbif")
@click.argument("gbif_id", type=click.INT)
@click.option("-v", "--verbose", is_flag=True, default=False)
def report_gbif(gbif_id: int, verbose: bool = False):
    data = get_gbif_data(gbif_id)
    print_report(data, verbose=verbose)


@cli.command("check-url")
@click.argument("url", type=click.STRING)
def check_url(url: str):
    data = get_data_from_url(url)
    if data is None:
        print(f"No JSON data could be loaded from the URL {url}")
    else:
        print_check(data)


@cli.command("check-file")
@click.argument("file", type=click.File())
def check_file(path: Path):
    with path.open() as f:
        print_check(json.load(f))


@cli.command("check-gbif")
@click.argument("gbif_id", type=click.INT)
def check_gbif(gbif_id: int):
    gbif_data = get_gbif_data(gbif_id)
    if gbif_data is None:
        print(f"No occurrence with ID {gbif_id} found")
    else:
        print_check(gbif_data)


if __name__ == "__main__":
    cli()
