import json
from pathlib import Path

import click
import httpx
import requests

from mids.lib import init
from mids.model import Discipline


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


def print_report(data: dict, verbose: bool = False):
    """
    Given some data, check it against MIDS and print a report to stdout.

    :param data: the data to report
    :param verbose: whether to print a verbose report or not (default: False)
    """
    report = init(Discipline.biology).report(data)

    if verbose:
        messages = {True: "PASS", False: "FAIL"}
        for result in report:
            print(f"Level {result.level}: {messages[result.passed]}")
            for element, passed in result:
                print(f"\t{element.name}: {messages[passed]}")
    else:
        for result in report:
            if result.passed:
                print(f"Level {result.level} passed")
            else:
                failed = ", ".join(element.name for element in result.fails)
                print(f"Level {result.level} failed on {failed}")


def print_check(data: dict):
    """
    Given some data, check it against MIDS and print the MIDS level of the data to
    stdout.

    :param data: the data to report
    """
    level = init(Discipline.biology).check(data)
    print(f"Matched to MIDS level {level}")


if __name__ == "__main__":
    cli()
