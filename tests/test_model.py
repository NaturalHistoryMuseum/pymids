from itertools import repeat, chain
from unittest.mock import MagicMock, Mock

import pytest

from mids.matchers import ExactMatcher
from mids.model import (
    CurieMap,
    Identifier,
    MIDSLevel,
    MIDSResult,
    MIDSElement,
    MIDSReport,
)


def test_curie_map():
    curie_map = CurieMap(
        {
            "ac": "http://rs.tdwg.org/ac/terms/",
            "dc": "http://purl.org/dc/terms/",
            "dwc": "http://rs.tdwg.org/dwc/terms/",
        }
    )
    assert curie_map["dc:Llama"] == Identifier(
        f"{curie_map.map['dc']}Llama", "Llama", "dc"
    )
    with pytest.raises(KeyError):
        assert isinstance(curie_map["beans:Llama"], Identifier)


def test_mids_level_order():
    assert list(MIDSLevel) == [
        MIDSLevel.mids0,
        MIDSLevel.mids1,
        MIDSLevel.mids2,
        MIDSLevel.mids3,
    ]


class TestMIDSResult:
    def test_pass(self):
        elements = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        result = MIDSResult(MIDSLevel.mids1, list(zip(elements, repeat(True))))
        assert result.passed
        assert result.passes == elements
        assert not result.fails

    def test_fail(self):
        pass_elements = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        fail_elements = [MagicMock(), MagicMock()]
        result = MIDSResult(
            MIDSLevel.mids1,
            list(
                chain(
                    zip(pass_elements, repeat(True)), zip(fail_elements, repeat(False))
                )
            ),
        )
        assert not result.passed
        assert result.passes == pass_elements
        assert result.fails == fail_elements


class TestReport:
    def test_level_none(self):
        report = MIDSReport(
            MagicMock(),
            {
                MIDSLevel.mids0: MIDSResult(MIDSLevel.mids0, [(MagicMock(), False)]),
                MIDSLevel.mids1: MIDSResult(MIDSLevel.mids1, [(MagicMock(), False)]),
                MIDSLevel.mids2: MIDSResult(MIDSLevel.mids2, [(MagicMock(), False)]),
                MIDSLevel.mids3: MIDSResult(MIDSLevel.mids3, [(MagicMock(), False)]),
            },
        )
        assert report.level is None

    def test_level_0(self):
        report = MIDSReport(
            MagicMock(),
            {
                MIDSLevel.mids0: MIDSResult(MIDSLevel.mids0, [(MagicMock(), True)]),
                MIDSLevel.mids1: MIDSResult(MIDSLevel.mids1, [(MagicMock(), False)]),
                MIDSLevel.mids2: MIDSResult(MIDSLevel.mids2, [(MagicMock(), False)]),
                MIDSLevel.mids3: MIDSResult(MIDSLevel.mids3, [(MagicMock(), False)]),
            },
        )
        assert report.level == MIDSLevel.mids0

    def test_level_1(self):
        report = MIDSReport(
            MagicMock(),
            {
                MIDSLevel.mids0: MIDSResult(MIDSLevel.mids0, [(MagicMock(), True)]),
                MIDSLevel.mids1: MIDSResult(MIDSLevel.mids1, [(MagicMock(), True)]),
                MIDSLevel.mids2: MIDSResult(MIDSLevel.mids2, [(MagicMock(), False)]),
                MIDSLevel.mids3: MIDSResult(MIDSLevel.mids3, [(MagicMock(), False)]),
            },
        )
        assert report.level == MIDSLevel.mids1

    def test_level_2(self):
        report = MIDSReport(
            MagicMock(),
            {
                MIDSLevel.mids0: MIDSResult(MIDSLevel.mids0, [(MagicMock(), True)]),
                MIDSLevel.mids1: MIDSResult(MIDSLevel.mids1, [(MagicMock(), True)]),
                MIDSLevel.mids2: MIDSResult(MIDSLevel.mids2, [(MagicMock(), True)]),
                MIDSLevel.mids3: MIDSResult(MIDSLevel.mids3, [(MagicMock(), False)]),
            },
        )
        assert report.level == MIDSLevel.mids2

    def test_level_3(self):
        report = MIDSReport(
            MagicMock(),
            {
                MIDSLevel.mids0: MIDSResult(MIDSLevel.mids0, [(MagicMock(), True)]),
                MIDSLevel.mids1: MIDSResult(MIDSLevel.mids1, [(MagicMock(), True)]),
                MIDSLevel.mids2: MIDSResult(MIDSLevel.mids2, [(MagicMock(), True)]),
                MIDSLevel.mids3: MIDSResult(MIDSLevel.mids3, [(MagicMock(), True)]),
            },
        )
        assert report.level == MIDSLevel.mids3


class TestMIDSElement:
    def test_name(self):
        element_identifier = Identifier("elemid", "elemname", "elemprefix")
        match_identifier = Identifier("matchid", "matchname", "matchprefix")

        element = MIDSElement(
            element_identifier, MIDSLevel.mids1, [ExactMatcher(match_identifier)]
        )
        assert element.name == element_identifier.name

    def test_match(self):
        element_identifier = Identifier("elemid", "elemname", "elemprefix")
        matchers = [
            ExactMatcher(Identifier(Mock(), "field1", Mock())),
            ExactMatcher(Identifier(Mock(), "field2", Mock())),
            ExactMatcher(Identifier(Mock(), "field3", Mock())),
            ExactMatcher(Identifier(Mock(), "field4", Mock())),
        ]

        element = MIDSElement(element_identifier, MIDSLevel.mids1, matchers)

        assert element.match({"field1": "beans"})
        assert element.match({"field2": "beans"})
        assert element.match({"field3": "beans"})
        assert element.match({"field4": "beans"})
        assert not element.match({"field5": "beans"})
        assert not element.match({"": "beans"})
