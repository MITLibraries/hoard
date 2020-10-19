import datetime
from typing import Iterable, Optional, Protocol, TypedDict


class Author(TypedDict):
    kerb: str
    name: str
    orcid: Optional[str]
    dlc: str
    start_date: datetime.date
    end_date: datetime.date


class Searchable(Protocol):
    def find(
        self, last_name: str, first_name: str = "", middle_name: str = ""
    ) -> Iterable[Author]:
        ...
