from bs4 import BeautifulSoup  # type: ignore
import requests
from typing import Iterator


from hoard.client import DataverseClient, DSpaceClient, OAIClient
from hoard.models import create_from_dataverse_json, Dataset


class JPAL:
    def __init__(self, client: OAIClient) -> None:
        self.client = client
        self.session = requests.Session()

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        record = next(self.client)
        xml = BeautifulSoup(record, "html.parser")
        json_url = xml.metadata["directapicall"]
        dataverse_json = self.session.get(json_url).json()
        dataset = create_from_dataverse_json(dataverse_json)
        return dataset


class RDR:
    def __init__(self, client: DataverseClient) -> None:
        self.client = client

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        ...


class WHOAS:
    def __init__(self, client: DSpaceClient) -> None:
        self.client = client

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        ...
