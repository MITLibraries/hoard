from sqlalchemy import (  # type: ignore
    Column,
    create_engine,
    ForeignKey,
    MetaData,
    String,
    Table,
    Unicode,
)


metadata = MetaData()


authors = Table(
    "library_person_lookup",
    metadata,
    Column("mit_id", String),
    Column("first_name", Unicode),
    Column("middle_name", Unicode),
    Column("last_name", Unicode),
    Column("full_name", Unicode),
    Column("krb_name", String),
    Column("email", String),
)


orcids = Table(
    "orcid_to_mitid",
    metadata,
    Column("mit_id", String, ForeignKey("library_person_lookup.mit_id")),
    Column("orcid", String),
)


class Engine:
    __engine = None

    def __call__(self):
        return self.__engine

    def configure(self, conn_string):
        self.__engine = self.__engine or create_engine(conn_string)


engine = Engine()
