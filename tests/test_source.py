import requests_mock
from unittest.mock import MagicMock

from hoard.source import JPAL, WHOAS


def test_jpal_returns_datasets(
    dataset, dataverse_minimal_json_record, dataverse_oai_xml_records
):
    oai_client = MagicMock()
    oai_client.__next__.return_value = next(iter(dataverse_oai_xml_records))
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/api/datasets/export?"
            "exporter=dataverse_json&persistentId=12345",
            json=dataverse_minimal_json_record,
        )
        jpal = JPAL(oai_client)
        assert next(jpal) == dataset


def test_whoas_returns_datasets(dspace_oai_xml_records):
    oai_client = MagicMock()
    oai_client.__next__.return_value = next(iter(dspace_oai_xml_records))
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/oai", text=dspace_oai_xml_records[0],
        )
        whoas = WHOAS(oai_client)
        assert (
            next(whoas).title == "The Title"
        )  # Not sure how deep we want to go with the testing
