from typing import Iterable, Tuple

from hoard.names.types import Author, Searchable


class AuthorService:
    def __init__(self, repository: Searchable) -> None:
        self.repository = repository

    def find(self, name: str) -> Iterable[Tuple[str, Author]]:
        for result in self.repository.find(*parse(name)):
            yield (name, result)


def parse(name: str) -> Tuple[str, str, str]:
    """Parse a name into constituent parts.

    The returned tuple is ordered like: (last, first, middle).
    """
    parts = name.split()
    last = parts.pop()
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
