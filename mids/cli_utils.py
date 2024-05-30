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
