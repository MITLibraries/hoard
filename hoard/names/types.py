from typing import Iterable, Protocol
from typing_extensions import TypedDict


class Author(TypedDict):
    kerb: str
    full_name: str
    orcid: str


class Searchable(Protocol):
    def find(
        self, last_name: str, first_name: str = "", middle_name: str = ""
    ) -> Iterable[Author]:
        ...
