from typing import Optional

import click

from hoard.api import Api
from hoard.client import DataverseClient, DataverseKey, OAIClient, Transport
from hoard.source import JPAL


@click.group()
def main():
    pass


@main.command()
@click.argument("source", type=click.Choice(["jpal"], case_sensitive=False))
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
def ingest(
    source: str, source_url: str, key: Optional[str], url: str, parent: str,
    format: str, set: str
) -> None:
    rdr = DataverseClient(Api(url, DataverseKey(key)), Transport())
    if source == "jpal":
        client = OAIClient(source_url, format, set)
    records = JPAL(client)
    for record in records:
        rdr.create(record, parent=parent)
