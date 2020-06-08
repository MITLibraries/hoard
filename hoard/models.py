import attr


@attr.s(auto_attribs=True)
class Dataset:
    title: str

    def asdict(self) -> dict:
        return attr.asdict(self)


def create_from_dict(data: dict) -> Dataset:
    title = data["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0][
        "value"
    ]
    return Dataset(title=title)
