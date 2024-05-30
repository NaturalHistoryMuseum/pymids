from collections import defaultdict
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter

from mids.io import read_metadata, read_mapping
from mids.matchers import NarrowMatcher, ExactMatcher, IntersectionOfMatcher
from mids.model import (
    CurieMap,
    MIDSLevel,
    MIDSElement,
    MIDSReport,
    MIDSResult,
    Discipline,
)


def init(discipline: Discipline) -> "MIDS":
    """
    Initialize a MIDS object for the given discipline.

    :param discipline: the discipline to initialize for
    :return: a MIDS object
    """
    metadata = read_metadata(discipline)
    mapping = sorted(read_mapping(discipline), key=itemgetter("subject_id"))
    curie_map = CurieMap(metadata["curie_map"])
    levels = defaultdict(list)

    for subject_id, rows_iter in groupby(mapping, key=itemgetter("subject_id")):
        rows = list(rows_iter)
        matchers = []

        for row in rows:
            predicate_id = curie_map[row["predicate_id"]]
            object_id = curie_map[row["object_id"]]

            if predicate_id.name == "narrowMatch":
                matchers.append(NarrowMatcher(object_id))
            elif predicate_id.name == "exactMatch":
                matchers.append(ExactMatcher(object_id))
            elif predicate_id.name == "intersectionOf":
                object_match_fields = row["object_match_field"]
                if object_match_fields:
                    object_ids = [
                        curie_map[object_id]
                        for object_id in object_match_fields.split("|")
                    ]
                    matchers.append(IntersectionOfMatcher(object_ids))
            else:
                raise Exception(f"Unknown predicate {predicate_id}")

        element_id = curie_map[rows[0]["subject_id"]]
        level = MIDSLevel[rows[0]["subject_category"]]
        element = MIDSElement(element_id, level, matchers)
        levels[element.level].append(element)

    return MIDS(discipline, curie_map, levels)


@dataclass
class MIDS:
    """
    Entry point for doing MIDS calculations.
    """

    discipline: Discipline
    curie_map: CurieMap
    levels: dict[MIDSLevel, list[MIDSElement]]

    def report(self, data: dict) -> MIDSReport:
        """
        Checks the given record data dict against the levels and elements specified in
        this object. All levels are checked, even if earlier ones have already failed so
        that a full report is created.

        :param data: the record data to check
        :return: a report about the performance of the record against MIDS
        """
        results = {
            level: MIDSResult(
                level=level,
                elements=[(element, element.match(data)) for element in elements],
            )
            for level, elements in self.levels.items()
        }
        return MIDSReport(data, results)

    def check(self, data: dict) -> MIDSLevel | None:
        """
        Checks the given record data dict against the levels and elements specified in
        this object, returning the MIDSLevel appropriate for the data. If the data
        doesn't meet the first MIDS level in use, None is returned.

        :param data: the record data to check
        :return: the MIDSLevel appropriate for the data
        """
        matched = None
        for level in MIDSLevel:
            # must match all elements to meet the level
            if all(element.match(data) for element in self.levels[level]):
                matched = level
            else:
                break
        return matched
