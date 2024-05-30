import abc
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum, auto
from functools import cached_property
from typing import Iterator, Iterable


class Discipline(StrEnum):
    """
    Enum representing the possible available disciplines.
    """

    # just biology at the moment
    biology = auto()


@dataclass
class Identifier:
    """
    Represents an identifier anywhere in the SSSOM mapping.
    """

    # the full ID (e.g. http://rs.tdwg.org/dwc/terms/occurrenceID)
    id: str
    # the name part of the ID (e.g. occurrenceID)
    name: str
    # the prefix in the curie map used to create the full ID (e.g. dwc)
    prefix: str

    def __str__(self) -> str:
        return self.id


@dataclass
class CurieMap:
    """
    Represents the curie map contained in the metadata YML file.
    """

    map: dict[str, str]

    def __getitem__(self, prefixed_id: str) -> Identifier:
        """
        Given a prefixed identifier, converts it into a full Identifier object using the
        contained curie map to lookup the prefix.

        :param prefixed_id: the prefixed identifier, such as dwc:occurrenceID
        :return: an Identifier object
        """
        prefix, name = prefixed_id.strip().split(":", 1)
        return Identifier(f"{self.map[prefix]}{name}", name, prefix)


class MIDSLevel(IntEnum):
    """
    Enum representing the MIDS levels.
    """

    mids0 = 0
    mids1 = 1
    mids2 = 2
    mids3 = 3


@dataclass
class MIDSElement:
    """
    Represents a single MIDS information element.
    """

    # the identifier for the element
    identifier: Identifier
    # the MIDS level this element applies to
    level: MIDSLevel
    # a list of Matcher objects to check data against
    matchers: list["Matcher"]

    @property
    def name(self) -> str:
        """
        The name of the MIDS information element.

        :return: the name
        """
        return self.identifier.name

    def match(self, data: dict) -> bool:
        """
        Runs the data through the matchers to determine if this element is present. If
        any of the matchers match the data then this will return True. Otherwise, False.

        :param data: the data to check
        :return: True if the element is present, False otherwise
        """
        return any(matcher(data) for matcher in self.matchers)


class Matcher(abc.ABC):
    """
    Abstract class representing a matcher for a specific criteria.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Matcher: {self.name}"

    @abc.abstractmethod
    def __call__(self, data: dict) -> bool:
        """
        Match against the given data and return True if the data matches this Matcher's
        criteria, or False if not.

        :param data: the record data
        :return: True if matched, False if not
        """
        ...


@dataclass
class MIDSResult:
    """
    Class representing the checks performed at a specific MIDS level.
    """

    level: MIDSLevel
    # all the elements in 2-tuples containing the element and a bool indicating if it
    # was passed or not
    elements: list[tuple[MIDSElement, bool]]

    @cached_property
    def passed(self) -> bool:
        """
        Returns True if all the elements were passed at this level by the data, or False
        if not.

        :return: True if the level was passed, False if not
        """
        return not self.fails

    @cached_property
    def fails(self) -> list[MIDSElement]:
        """
        Returns the elements that were failed at this level.

        :return: a list of MIDSElements with failed checks
        """
        return [element for element, matched in self.elements if not matched]

    @cached_property
    def passes(self) -> list[MIDSElement]:
        """
        Returns the elements that were passed at this level.

        :return: a list of MIDSElements with passed checks
        """
        return [element for element, matched in self.elements if matched]

    def __iter__(self) -> Iterable[tuple[MIDSElement, bool]]:
        yield from self.elements


@dataclass
class MIDSReport:
    """
    A report about the checks that have been performed against the given data.
    """

    # the data that was assessed
    data: dict
    # the results that came from the checks
    results: dict[MIDSLevel, MIDSResult]

    @property
    def level(self) -> MIDSLevel | None:
        """
        Returns the MIDS level of the data this report covers. If the data doesn't meet
        the minimum lowest MIDS level, None is returned.

        :return: the MIDS level for the data
        """
        matched = None
        for level in MIDSLevel:
            # must match all elements to meet the level
            if self.results[level].passed:
                matched = level
            else:
                break
        return matched

    def __getitem__(self, level: MIDSLevel) -> MIDSResult:
        """
        Returns the result for the given MIDS level.

        :param level: the MIDS level
        :return: the result
        """
        return self.results[level]

    def __iter__(self) -> Iterator[MIDSResult]:
        """
        Yields the results for each MIDS level starting at MIDS level 0 and increasing
        up to MIDS level 3.

        :return: a generator of MIDSResult objects
        """
        yield from map(self.__getitem__, MIDSLevel)
