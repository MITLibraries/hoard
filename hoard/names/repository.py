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
                [
                    authors.c.krb_name_uppercase.label("kerb"),
                    authors.c.full_name.label("name"),
                    orcids.c.orcid,
                    authors.c.hr_org_unit_title.label("dlc"),
                    authors.c.original_hire_date.label("start_date"),
                    authors.c.appointment_end_date.label("end_date"),
                ]
            )
            .select_from(authors.outerjoin(orcids))
            .where(and_(*query))
            .limit(10)
        )
        with closing(self.engine.connect()) as conn:
            yield from (
                Author(
                    kerb=row.kerb,
                    name=row.name,
                    orcid=row.orcid,
                    dlc=row.dlc,
                    start_date=row.start_date,
                    end_date=row.end_date,
                )
                for row in conn.execute(sql)
            )
