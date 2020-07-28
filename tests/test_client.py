import requests_mock

from hoard.api import Api
from hoard.client import DataverseClient, DataverseKey, Transport


def test_client_gets_dataset_by_id(dataverse_json_record):
    with requests_mock.Mocker() as m:
        m.get("http+mock://example.com/api/v1/datasets/666", json=dataverse_json_record)
        client = DataverseClient(Api("http+mock://example.com"), Transport())
        dv = client.get(id=666)
        assert dv == dataverse_json_record


def test_client_gets_dataset_by_pid(dataverse_json_record):
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/api/v1/datasets/:persistentId"
            "?persistentId=doi:foo/bar",
            json=dataverse_json_record,
        )
        client = DataverseClient(Api("http+mock://example.com"), Transport())
        dv = client.get(pid="doi:foo/bar")
        assert dv == dataverse_json_record


def test_client_creates_dataset(dataset):
    with requests_mock.Mocker() as m:
        m.post(
            "http+mock://example.com/api/v1/root/datasets",
            json={"data": {"id": 1, "persistentId": "set1"}},
        )
        client = DataverseClient(Api("http+mock://example.com/"), Transport())
        dv_id, p_id = client.create(dataset)
    assert m.last_request.json() == dataset.asdict()
    assert dv_id == 1
    assert p_id == "set1"


def test_client_adds_authentication(dataset):
    with requests_mock.Mocker() as m:
        m.post(
            "http+mock://example.com/api/v1/root/datasets",
            json={"data": {"id": 1, "persistentId": "set1"}},
        )
        api = Api("http+mock://example.com", DataverseKey("123"))
        client = DataverseClient(api, Transport())
        client.create(dataset)
    assert m.last_request.headers["X-Dataverse-key"] == "123"
