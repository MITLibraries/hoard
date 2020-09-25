from click.testing import CliRunner

from hoard.cli import main


def test_cli_jpal_ingests(requests_mock, jpal_oai_server, jpal_dataverse_server):
    requests_mock.post(
        "http+mock://example.com/api/v1/dataverses/root/datasets",
        [
            {"json": {"data": {"id": 1, "persistentId": "set1"}}, "status_code": 200},
            {"text": "Dataverse json parsing error", "status_code": 400},
        ],
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
    assert "1 records ingested from jpal\n" in result.output
    assert "HTTP error: 400" in result.output


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
