import json
from pathlib import Path

import click
import httpx
import requests

from mids.cli_utils import print_check, print_report


@click.group("mids")
def cli():
    pass


@cli.command("report-url")
@click.argument("url", type=click.STRING)
@click.option("-v", "--verbose", is_flag=True, default=False)
def report_url(url: str, verbose: bool = False):
    with requests.get(url) as r:
        print_report(r.json(), verbose=verbose)


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
    gbif_url = f"https://api.gbif.org/v1/occurrence/{gbif_id}"
    response = httpx.get(gbif_url)
    print_report(response.json(), verbose=verbose)


@cli.command("check-url")
@click.argument("url", type=click.STRING)
def check_url(url: str):
    with requests.get(url) as r:
        print_check(r.json())


@cli.command("check-file")
@click.argument("file", type=click.File())
@click.option("-v", "--verbose", is_flag=True, default=False)
def check_file(path: Path, verbose: bool = False):
    with path.open() as f:
        print_check(json.load(f))


@cli.command("check-gbif")
@click.argument("gbif_id", type=click.INT)
@click.option("-v", "--verbose", is_flag=True, default=False)
def check_gbif(gbif_id: int, verbose: bool = False):
    gbif_url = f"https://api.gbif.org/v1/occurrence/{gbif_id}"
    response = httpx.get(gbif_url)
    print_check(response.json())


if __name__ == "__main__":
    cli()
