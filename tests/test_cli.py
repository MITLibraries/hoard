from click.testing import CliRunner

from hoard.cli import main


def test_cli_ingests(requests_mock, jpal_oai_server, jpal_dataverse_server):
    requests_mock.post(
        "http+mock://example.com/api/v1/dataverses/root/datasets",
        json={"data": {"id": 1, "persistentId": "set1"}},
    )
    result = CliRunner().invoke(
        main,
        [
            "ingest",
            "jpal",
            "http+mock://example.com/oai",
            "--url",
            "http+mock://example.com",
        ],
    )
    assert result.exit_code == 0
    assert result.output == "2 records ingested from jpal\n"


def test_cli_whoas_ingests(requests_mock, whoas_oai_server):
    requests_mock.post(
        "http+mock://example.com/api/v1/dataverses/root/datasets",
        json={"data": {"id": 1, "persistentId": "set1"}},
    )
    result = CliRunner().invoke(
        main,
        [
            "ingest",
            "whoas",
            "http+mock://example.com/oai",
            "--url",
            "http+mock://example.com",
        ],
    )
    assert result.exit_code == 0
    assert result.output == "2 records ingested from whoas\n"
