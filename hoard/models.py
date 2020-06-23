import attr


@attr.s(auto_attribs=True)
class Dataset:
    title: str

    def asdict(self) -> dict:
        return attr.asdict(self)


def create_whoas(item):
    return Dataset(...)


def create_rdr(item: dict) -> Dataset:
    title = item["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0][
        "value"
    ]
    return Dataset(title=title)
