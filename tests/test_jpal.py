import requests_mock
from unittest.mock import MagicMock

from hoard.sources.jpal import create_from_dataverse_json, JPAL


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


def test_create_dataset_from_dataverse_json(dataverse_minimal_json_record):
    dataset = create_from_dataverse_json(dataverse_minimal_json_record)
    assert dataset.asdict() == dataverse_minimal_json_record
