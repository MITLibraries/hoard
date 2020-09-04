from typing import Iterator, TextIO

from hoard.models import Dataset


class LincolnLab:
    def __init__(self, stream: TextIO) -> None:
        self.stream = stream

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        ...
