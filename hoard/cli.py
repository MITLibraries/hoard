import logging
import sys
from typing import Iterator, Optional

import click
from smart_open import open  # type: ignore
import requests
import structlog  # type: ignore

from hoard.api import Api
from hoard.client import DataverseClient, DataverseKey, OAIClient, Transport
from hoard.models import Dataset
from hoard.names import AuthorService, engine, Warehouse
from hoard.sources import JPAL, LincolnLab, WHOAS


@click.group()
def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(pad_event=0),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


@main.command()
@click.argument(
    "source", type=click.Choice(["jpal", "llab", "whoas"], case_sensitive=False)
)
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
    elif source == "whoas":
        client = OAIClient(source_url, "dim", "com_1912_4134")
        records = WHOAS(client)
    for record in records:
        try:
            dv_id, p_id = rdr.create(record, parent=parent)
            if verbose:
                click.echo(f"Created {p_id}")
            count += 1
        except requests.HTTPError as e:
            click.echo(
                f"Unable to ingest record. HTTP error: {e}."
                f"Dataverse response: {e.response.text}"
            )
    click.echo(f"{count} records ingested from {source}")


def pipe(ctx, param, value):
    if not value:
        return (line.rstrip() for line in click.get_text_stream("stdin"))
    else:
        return value


@main.command()
@click.argument("authors", nargs=-1, callback=pipe)
@click.option("--database", help="SQLAlchemy DB connection string")
def author(authors, database) -> None:
    """Search for one or more authors.

    Can be used to query the data warehouse for an author.
    """
    engine.configure(database)
    svc = AuthorService(Warehouse(engine()))
    for author in authors:
        click.echo(author)
        results = svc.find(author)
        for result in results:
            name = result[1]["name"]
            kerb = result[1]["kerb"]
            dlc = result[1]["dlc"]
            click.echo(f"\t{name} ({kerb})\t{dlc}")
