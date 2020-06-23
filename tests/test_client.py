import pytest
import requests_mock

from hoard.api import Api
from hoard.client import Client, Transport, DataverseKey
from hoard.models import Dataset, create_rdr


@pytest.fixture
def response():
    resp = {
        "data": {
            "latestVersion": {
                "metadataBlocks": {
                    "citation": {
                        "fields": [{"typeName": "title", "value": "The Hoard"}]
                    }
                }
            }
        }
    }
    return resp


def test_client_gets_dataset_by_id(response):
    with requests_mock.Mocker() as m:
        m.get("http+mock://example.com/api/v1/datasets/666", json=response)
        client = Client(Api("http+mock://example.com"), Transport(), create_rdr)
        dv = client.get(id=666)
        assert dv.title == "The Hoard"


def test_client_gets_dataset_by_pid(response):
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/api/v1/datasets/:persistentId"
            "?persistentId=doi:foo/bar",
            json=response,
        )
        client = Client(Api("http+mock://example.com"), Transport(), create_rdr)
        dv = client.get(pid="doi:foo/bar")
        assert dv.title == "The Hoard"


def test_client_creates_dataset():
    record = Dataset(title="whatever")
    with requests_mock.Mocker() as m:
        m.post(
            "http+mock://example.com/api/v1/root/datasets",
            json={"data": {"id": 1, "persistentId": "set1"}},
        )
        client = Client(Api("http+mock://example.com/"), Transport(), create_rdr)
        dv_id, p_id = client.create(record)
    assert m.last_request.json() == record.asdict()
    assert dv_id == 1
    assert p_id == "set1"


def test_client_adds_authentication():
    with requests_mock.Mocker() as m:
        m.post(
            "http+mock://example.com/api/v1/root/datasets",
            json={"data": {"id": 1, "persistentId": "set1"}},
        )
        api = Api("http+mock://example.com", DataverseKey("123"))
        client = Client(api, Transport(), create_rdr)
        client.create(Dataset(title="whatever"))
    assert m.last_request.headers["X-Dataverse-key"] == "123"
