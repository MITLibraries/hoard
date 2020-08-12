from typing import Iterator, Optional

import click
from smart_open import open  # type: ignore

from hoard.api import Api
from hoard.client import DataverseClient, DataverseKey, OAIClient, Transport
from hoard.models import Dataset
from hoard.source import JPAL, LincolnLab


@click.group()
def main():
    pass


@main.command()
@click.argument("source", type=click.Choice(["jpal", "llab"], case_sensitive=False))
@click.argument("source_url")
@click.option("--key", "-k", help="RDR authentication key.")
@click.option(
    "--parent", "-p", default="root", help="Parent dataverse to ingest items into."
)
@click.option(
    "--url",
    "-u",
    default="http://localhost",
    help="URL for RDR. Records will be ingested into this system.",
)
@click.option("--verbose", "-v", is_flag=True)
def ingest(
    source: str,
    source_url: str,
    key: Optional[str],
    url: str,
    parent: str,
    verbose: bool,
) -> None:
    """Ingest a source into RDR.

    This will load items from the specified source located at SOURCE_URL
    into an RDR instance. SOURCE_URL can be either a URL or a local or S3
    file URL, e.g. file:///path/to/file, s3://bucket/key.
    """
    count = 0
    rdr = DataverseClient(Api(url, DataverseKey(key)), Transport())
    records: Iterator[Dataset]
    if source == "jpal":
        client = OAIClient(source_url, "dataverse_json", "Jameel_Poverty_Action_Lab")
        records = JPAL(client)
    elif source == "llab":
        stream = open(source_url)
        records = LincolnLab(stream)
    for record in records:
        dv_id, p_id = rdr.create(record, parent=parent)
        if verbose:
            click.echo(f"Created {p_id}")
        count += 1
    click.echo(f"{count} records ingested from {source}")
