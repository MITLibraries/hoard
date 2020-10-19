from sqlalchemy import (  # type: ignore
    Column,
    create_engine,
    Date,
    ForeignKey,
    MetaData,
    String,
    Table,
    Unicode,
)


metadata = MetaData()


authors = Table(
    "hr_person_employee_limited",
    metadata,
    Column("mit_id", String),
    Column("first_name", Unicode),
    Column("middle_name", Unicode),
    Column("last_name", Unicode),
    Column("full_name", Unicode),
    Column("krb_name_uppercase", String),
    Column("email", String),
    Column("hr_org_unit_title", String),
    Column("original_hire_date", Date),
    Column("appointment_end_date", Date),
)


orcids = Table(
    "orcid_to_mitid",
    metadata,
    Column("mit_id", String, ForeignKey("hr_person_employee_limited.mit_id")),
    Column("orcid", String),
)


class Engine:
    __engine = None

    def __call__(self):
        return self.__engine

    def configure(self, conn_string):
        self.__engine = self.__engine or create_engine(conn_string)


engine = Engine()
