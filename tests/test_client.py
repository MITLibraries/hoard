import requests_mock

from hoard.api import Api
from hoard.client import DataverseClient, DataverseKey, OAIClient, Transport


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


def test_oaiclient_get(shared_datadir):
    with requests_mock.Mocker() as m:
        ids_url = "http+mock://example.com/oai?verb=ListIdentifiers"
        ids_url += "&metadataPrefix=oai_dc&set=testcollection"
        ids_xml = (shared_datadir / "OAI_ListIdentifiers.xml").read_text()
        rec_url = "http+mock://example.com/oai?verb=GetRecord&identifier=1234"
        rec_url += "&metadataPrefix=oai_dc"
        rec_xml = (shared_datadir / "OAI_GetRecord.xml").read_text()
        m.get(ids_url, text=ids_xml)
        m.get(rec_url, text=rec_xml)
        source_url = "http+mock://example.com/oai"
        format = "oai_dc"
        set = "testcollection"
        records = OAIClient(source_url, format, set)
        for record in records:
            assert record == (shared_datadir / "OAI_GetRecord.xml").read_text()
