import csv
from pathlib import Path

import yaml

from mids.model import Discipline

sssom_path = Path(__file__).parent.parent / "sssom"


def read_mapping(discipline: Discipline) -> list[dict]:
    """
    Read the SSSOM TSV mapping file for the given discipline and return it.

    :param discipline: the discipline to read
    :return: a list of rows as dicts from the TSV
    """
    path = sssom_path / f"v0.1_{discipline}.sssom.tsv"
    with path.open() as f:
        return list(csv.DictReader(f, dialect="excel-tab"))


def read_metadata(discipline: Discipline) -> dict:
    """
    Read the SSSOM YML metadata file for the given discipline and return it.

    :param discipline: the discipline to read
    :return: a dict
    """
    path = sssom_path / f"v0.1_{discipline}.sssom.yml"
    with path.open() as f:
        return yaml.load(f, Loader=yaml.SafeLoader)
