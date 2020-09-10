from bs4 import BeautifulSoup  # type: ignore
import requests
from typing import List, Iterator


from hoard.client import OAIClient
from hoard.models import Author, Contact, Dataset, Description


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


def create_from_dataverse_json(data: dict) -> Dataset:
    fields = data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]
    title = [x["value"] for x in fields if x["typeName"] == "title"][0]
    authors = [get_authors(x["value"]) for x in fields if x["typeName"] == "author"][0]
    contacts = [
        get_contacts(x["value"]) for x in fields if x["typeName"] == "datasetContact"
    ][0]
    description = [
        get_descriptions(x["value"]) for x in fields if x["typeName"] == "dsDescription"
    ][0]
    subjects = [[v for v in x["value"]] for x in fields if x["typeName"] == "subject"][
        0
    ]

    return Dataset(
        title=title,
        authors=authors,
        contacts=contacts,
        description=description,
        subjects=subjects,
    )


def get_authors(values: dict) -> List[Author]:
    authors = []
    for v in values:
        author = Author(
            authorName=v["authorName"]["value"],
            authorAffiliation=v["authorAffiliation"]["value"],
        )
        authors.append(author)
    return authors


def get_contacts(values: dict) -> List[Contact]:
    contacts = []
    for v in values:
        contact = Contact(
            datasetContactName=v["datasetContactName"]["value"],
            datasetContactEmail=v["datasetContactEmail"]["value"],
        )
        contacts.append(contact)
    return contacts


def get_descriptions(values: dict) -> List[Description]:
    descriptions = []
    for v in values:
        description = Description(dsDescriptionValue=v["dsDescriptionValue"]["value"],)
        descriptions.append(description)
    return descriptions
