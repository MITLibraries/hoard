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
def dataverse_json_record():
    with open("fixtures/dataset-finch1.json") as f:
        r = json.load(f)
        return r


@pytest.fixture
def dataverse_oai_xml_records():
    records = ['<record><header><identifier>12345</identifier><datestamp>2020-01-01T01:01:11Z</datestamp><setSpec>cool_research_lab</setSpec></header><metadata directApiCall="http+mock://example.com/api/datasets/export?exporter=dataverse_json&persistentId=12345"/></record>']
    return records
