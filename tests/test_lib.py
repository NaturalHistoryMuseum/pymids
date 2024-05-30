from mids.lib import init, MIDS
from mids.model import Discipline


def test_can_be_loaded():
    mids = init(Discipline.biology)
    assert isinstance(mids, MIDS)


def test_check():
    mids = init(Discipline.biology)
    data = {}
