import json

import pytest

from hoard.models import Author, Contact, Dataset, Description


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
def dataverse_json_record(shared_datadir):
    f = (shared_datadir / "dataset-finch1.json").read_text()
    r = json.loads(f)
    return r


@pytest.fixture
def dataverse_oai_xml_records(shared_datadir):
    records = [(shared_datadir / "OAI_Record.xml").read_text()]
    return records


@pytest.fixture
def dspace_oai_xml_records(shared_datadir):
    records = [(shared_datadir / "DSpace_OAI_Record.xml").read_text()]
    return records


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
