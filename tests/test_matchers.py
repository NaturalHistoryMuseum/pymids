from mids.matchers import (
    ExactMatcher,
    EMPTY_VALUES,
    NarrowMatcher,
    IntersectionOfMatcher,
)
from mids.model import Identifier


def test_exact_matcher():
    matcher = ExactMatcher(
        Identifier("http://rs.tdwg.org/dwc/terms/occurrenceID", "occurrenceID", "dwc")
    )

    # pass
    assert matcher({"occurrenceID": "1234"})
    # fail - missing
    assert not matcher({"beans": "yep!"})
    # fail - empty values
    for empty_value in EMPTY_VALUES:
        assert not matcher({"occurrenceID": empty_value})


def test_narrow_matcher():
    matcher = NarrowMatcher(
        Identifier("http://rs.tdwg.org/dwc/terms/occurrenceID", "occurrenceID", "dwc")
    )

    # pass
    assert matcher({"occurrenceID": "1234"})
    # fail - missing
    assert not matcher({"beans": "yep!"})
    # fail - empty values
    for empty_value in EMPTY_VALUES:
        assert not matcher({"occurrenceID": empty_value})


def test_intersection_of_matcher():
    matcher = IntersectionOfMatcher(
        [
            Identifier(
                "http://rs.tdwg.org/dwc/terms/decimalLatitude",
                "decimalLatitude",
                "dwc",
            ),
            Identifier(
                "http://rs.tdwg.org/dwc/terms/decimalLongitude",
                "decimalLongitude",
                "dwc",
            ),
        ]
    )

    # pass
    assert matcher({"decimalLatitude": 10.4, "decimalLongitude": 130.7})
    # fail - missing
    assert not matcher({"beans": "yep!"})
    assert not matcher({"beans": "yep!", "decimalLongitude": 130.7})
    assert not matcher({"beans": "yep!", "decimalLatitude": 10.4})
    # fail - empty values
    for empty_value in EMPTY_VALUES:
        assert not matcher(
            {
                "beans": "yep!",
                "decimalLatitude": empty_value,
                "decimalLongitude": empty_value,
            }
        )
        assert not matcher({"beans": "yep!", "decimalLongitude": empty_value})
        assert not matcher({"beans": "yep!", "decimalLatitude": empty_value})
