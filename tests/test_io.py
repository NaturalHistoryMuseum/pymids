from mids.io import read_mapping, read_metadata
from mids.model import Discipline


def test_read_mapping():
    # just check that the file can be read and it contains stuff that looks ok
    mapping = read_mapping(Discipline.biology)
    assert mapping
    assert isinstance(mapping, list)
    assert isinstance(mapping[0], dict)


def test_read_metadata():
    # just check that the file can be read and it contains stuff that looks ok
    mapping = read_metadata(Discipline.biology)
    assert mapping
    assert isinstance(mapping, dict)
