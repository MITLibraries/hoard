from typing import Iterator

from hoard.client import DataverseClient, DSpaceClient
from hoard.models import Dataset


class JPAL:
    def __init__(self, client: DataverseClient) -> None:
        self.client = client

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        ...


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
