import json
import pathlib

import pytest

from hoard.models import Author, Contact, Dataset, Description
from hoard.names.db import authors, engine, metadata, orcids


@pytest.fixture
def dataset():
    author = Author(authorName="Finch, Fiona", authorAffiliation="Birds Inc.")
    contact = Contact(
        datasetContactName="Finch, Fiona", datasetContactEmail="finch@mailinator.com"
    )
    description = Description(
        dsDescriptionValue="Darwin's finches (also known"
        " as the Galápagos finches) are a group of about"
        " fifteen species of passerine birds."
    )
    dataset = Dataset(
        authors=[author],
        contacts=[contact],
        description=[description],
        subjects=["Medicine, Health and Life Sciences"],
        title="Darwin's Finches",
    )
    return dataset


@pytest.fixture
def dataverse_minimal_json_record(shared_datadir):
    f = (shared_datadir / "required_fields.json").read_text()
    r = json.loads(f)
    return r


@pytest.fixture
def dataverse_partial_json_record(shared_datadir):
    f = (shared_datadir / "partial_fields.json").read_text()
    r = json.loads(f)
    return r


@pytest.fixture
def dataverse_full_json_record(shared_datadir):
    f = (shared_datadir / "all_fields.json").read_text()
    r = json.loads(f)
    return r


@pytest.fixture
def dataverse_oai_xml_records(shared_datadir):
    records = [(shared_datadir / "OAI_Record.xml").read_text()]
    return records


@pytest.fixture
def dspace_oai_xml_series_name_record(shared_datadir):
    record = (shared_datadir / "whoas/GetRecordSeriesName.xml").read_text()
    return record


@pytest.fixture
def jpal_oai_server(requests_mock, shared_datadir, request):
    url = "http+mock://example.com/oai"
    records = {
        "doi:10.7910/DVN/16OAH0": (
            shared_datadir / "jpal/GetRecord_01.xml"
        ).read_text(),
        "doi:10.7910/DVN/19PPE7": (
            shared_datadir / "jpal/GetRecord_02.xml"
        ).read_text(),
        "doi:10.7910/DVN/2ELQNE": (
            shared_datadir / "jpal/GetRecord_03.xml"
        ).read_text(),
        "doi:10.7910/DVN/4IYQLO": (
            shared_datadir / "jpal/GetRecord_04.xml"
        ).read_text(),
    }
    requests_mock.get(
        f"{url}?verb=ListIdentifiers",
        text=(shared_datadir / "jpal/ListRecords.xml").read_text(),
    )
    for k, v in records.items():
        requests_mock.get(f"{url}?identifier={k}", text=v)
    return [records["doi:10.7910/DVN/19PPE7"], records["doi:10.7910/DVN/2ELQNE"]]


@pytest.fixture
def whoas_oai_server(requests_mock, shared_datadir, request):
    url = "http+mock://example.com/oai"
    records = {
        "oai:darchive.mblwhoilibrary.org:1912/2367": (
            shared_datadir / "whoas/GetRecord_01.xml"
        ).read_text(),
        "oai:darchive.mblwhoilibrary.org:1912/2368": (
            shared_datadir / "whoas/GetRecord_02.xml"
        ).read_text(),
        "oai:darchive.mblwhoilibrary.org:1912/2369": (
            shared_datadir / "whoas/GetRecord_03.xml"
        ).read_text(),
        "oai:darchive.mblwhoilibrary.org:1912/2370": (
            shared_datadir / "whoas/GetRecord_04.xml"
        ).read_text(),
        "oai:darchive.mblwhoilibrary.org:1912/2371": (
            shared_datadir / "whoas/GetRecord_05.xml"
        ).read_text(),
        "oai:darchive.mblwhoilibrary.org:1912/2372": (
            shared_datadir / "whoas/GetRecord_06.xml"
        ).read_text(),
    }
    requests_mock.get(
        f"{url}?verb=ListIdentifiers",
        text=(shared_datadir / "whoas/ListRecords.xml").read_text(),
    )
    for k, v in records.items():
        requests_mock.get(f"{url}?identifier={k}", text=v)
    return [
        records["oai:darchive.mblwhoilibrary.org:1912/2367"],
        records["oai:darchive.mblwhoilibrary.org:1912/2368"],
        records["oai:darchive.mblwhoilibrary.org:1912/2369"],
        records["oai:darchive.mblwhoilibrary.org:1912/2370"],
        records["oai:darchive.mblwhoilibrary.org:1912/2371"],
        records["oai:darchive.mblwhoilibrary.org:1912/2372"],
    ]


@pytest.fixture
def jpal_dataverse_server(requests_mock, shared_datadir):
    url = "http+mock://example.com/api/datasets/export"
    records = {
        "doi:10.7910/DVN/19PPE7": "jpal/Record2.json",
        "doi:10.7910/DVN/2ELQNE": "jpal/Record3.json",
    }
    for k, v in records.items():
        requests_mock.get(
            f"{url}?persistentId={k}", text=(shared_datadir / v).read_text()
        )


@pytest.fixture
def db():
    engine.configure("sqlite://")
    metadata.create_all(engine())
    yield
    metadata.drop_all(engine())


@pytest.fixture
def warehouse_data(db):
    #  The shared_data pytest plugin seems kind of broken with sub-packages.
    #  Hence, dropping back into stdlib for fixtures here.
    c = pathlib.Path(__file__).parent.absolute()
    with open(c / "data/warehouse.json") as fp:
        data = json.load(fp)
    with engine().connect() as conn:
        conn.execute(authors.insert(), data["authors"])
        conn.execute(orcids.insert(), data["orcids"])
