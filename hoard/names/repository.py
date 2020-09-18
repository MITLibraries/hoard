from contextlib import closing
from typing import Iterable

from sqlalchemy import and_, select  # type: ignore

from hoard.names.db import authors, orcids
from hoard.names.types import Author


class Warehouse:
    def __init__(self, engine) -> None:
        self.engine = engine

    def find(self, last: str, first: str = "", middle: str = "") -> Iterable[Author]:
        query = []
        query.append(authors.c.last_name == last)
        if first:
            query.append(authors.c.first_name.like(first + "%"))
        if middle:
            query.append(authors.c.middle_name.like(middle[0] + "%"))
        sql = (
            select(
                [authors.c.krb_name.label("kerb"), authors.c.full_name, orcids.c.orcid]
            )
            .select_from(authors.outerjoin(orcids))
            .where(and_(*query))
        )
        with closing(self.engine.connect()) as conn:
            yield from conn.execute(sql)
