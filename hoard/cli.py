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
@click.option("--verbose", "-v", is_flag=True)
def ingest(
    source: str,
    source_url: str,
    key: Optional[str],
    url: str,
    parent: str,
    verbose: bool,
) -> None:
    count = 0
    rdr = DataverseClient(Api(url, DataverseKey(key)), Transport())
    if source == "jpal":
        client = OAIClient(source_url, "dataverse_json", "Jameel_Poverty_Action_Lab")
    records = JPAL(client)
    for record in records:
        dv_id, p_id = rdr.create(record, parent=parent)
        if verbose:
            click.echo(f"Created {p_id}")
        count += 1
    click.echo(f"{count} records ingested from {source}")
