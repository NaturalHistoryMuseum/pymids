from dataclasses import dataclass

from mids.model import Identifier, Matcher

EMPTY_VALUES = {None, ""}


class ExactMatcher(Matcher):
    """
    Class representing an exact match.

    If the name of the identifier exists in the data and doesn't have a value from the
    EMPTY_VALUES set, the matcher will pass.
    """

    def __init__(self, identifier: Identifier):
        super().__init__(identifier.name)
        self.identifier = identifier

    def __call__(self, data: dict) -> bool:
        return data.get(self.identifier.name, None) not in EMPTY_VALUES


class NarrowMatcher(ExactMatcher):
    """
    Class representing a narrow match.

    This acts exactly the same as an exact match.
    """

    pass


class IntersectionOfMatcher(Matcher):
    """
    Class representing a match based on the presence of multiple identifiers.

    All identifiers have to be present in the data for this matcher to pass.
    """

    def __init__(self, identifiers: list[Identifier]):
        super().__init__(f"[{','.join(identifier.name for identifier in identifiers)}]")
        self.identifiers = identifiers
        # cache the names we're going to look up
        self._names = [identifier.name for identifier in identifiers]

    def __call__(self, data: dict):
        return all(data.get(name, None) not in EMPTY_VALUES for name in self._names)
