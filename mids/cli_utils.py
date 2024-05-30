import json
import urllib.request
from urllib.error import HTTPError

from mids.lib import init
from mids.model import Discipline


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


def get_gbif_data(gbif_id: int) -> dict | None:
    """
    Retrieves the data for the given GBIF ID from the GBIF API.

    :param gbif_id: the GBIF ID of the occurrence
    :return: either data as a dict or None if the occurrence does not exist
    """
    return get_data_from_url(f"https://api.gbif.org/v1/occurrence/{gbif_id}")


def get_data_from_url(url: str) -> dict | None:
    """
    Retrieves JSON data from the given URL and returns it, or None if the request fails.

    :param url: the URL to retrieve data from
    :return: either data as a dict or None if a response cannot be retrieved
    """
    try:
        with urllib.request.urlopen(url) as r:
            if r.headers["Content-Type"] != "application/json":
                return None
            data = r.read().decode("utf-8")
            return json.loads(data)
    except HTTPError:
        return None
