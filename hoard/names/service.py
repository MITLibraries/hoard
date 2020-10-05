from typing import Iterable, Tuple

from hoard.names.logging import log
from hoard.names.types import Author, Searchable


class AuthorService:
    def __init__(self, repository: Searchable) -> None:
        self.repository = repository

    @log
    def find(self, name: str) -> Iterable[Tuple[str, Author]]:
        for result in self.repository.find(*parse(name)):
            yield (name, result)


def parse(name: str) -> Tuple[str, str, str]:
    """Parse a name into constituent parts.

    This assumes the name is of the form:

        last, first middle

    If there is no comma, it will treat the entire string as the last name.
    The returned tuple is ordered like: (last, first, middle).
    """
    last, *rest = name.split(",")
    if not rest:
        return last, "", ""
    parts = rest[0].split()
    parts.reverse()
    try:
        first = parts.pop()
    except IndexError:
        first = ""
    try:
        middle = parts.pop()
    except IndexError:
        middle = ""
    return last, first, middle
