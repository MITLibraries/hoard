from typing import Any, Dict, List, Optional

import attr
import xml.etree.ElementTree as ET


@attr.s(auto_attribs=True)
class Author:
    authorName: str
    authorAffiliation: str
    authorIdentifierScheme: Optional[str] = None
    authorIdentifierValue: Optional[str] = None


@attr.s(auto_attribs=True)
class Contact:
    datasetContactName: str
    datasetContactEmail: str
    datasetContactAffiliation: Optional[str] = None


@attr.s(auto_attribs=True)
class Description:
    dsDescriptionValue: str
    dsDescriptionDate: Optional[str] = None


@attr.s(auto_attribs=True)
class Dataset:
    authors: List[Author]
    contacts: List[Contact]
    description: List[Description]
    subjects: List[str]
    title: str

    def asdict(self) -> dict:
        fields = [primitive(self.title, "title")]
        fields.append(
            compound(
                self.authors,
                "author",
                [
                    "authorName",
                    "authorAffiliation",
                    "authorIdentifierScheme",
                    "authorIdentifierValue",
                ],
            )
        )
        fields.append(
            compound(
                self.contacts,
                "datasetContact",
                [
                    "datasetContactName",
                    "datasetContactEmail",
                    "datasetContactAffiliation",
                ],
            )
        )
        fields.append(
            compound(self.description, "dsDescription", ["dsDescriptionValue"])
        )
        fields.append(controlled(self.subjects, "subject"))

        result = {
            "datasetVersion": {
                "metadataBlocks": {
                    "citation": {"displayName": "Citation Metadata", "fields": fields}
                }
            }
        }

        return result


# Helper functions
def create_from_dublin_core_xml(data: str) -> Dataset:
    record = ET.fromstring(data)
    namespace = {
        "oai": "http://www.openarchives.org/OAI/2.0/",
        "dc": "http://purl.org/dc/elements/1.1/",
    }
    title_elem = record.find(".//dc:title", namespace)
    if title_elem is not None and title_elem.text is not None:
        title = title_elem.text
    authors = []
    for x in record.findall(".//dc:creator", namespace):
        if x.text is not None:
            authors.append(Author(authorName=x.text, authorAffiliation=""))
    contacts = [
        Contact(
            datasetContactName="NAME, FAKE",
            datasetContactEmail="FAKE_EMAIL@FAKE_DOMAIN.EDU",
        )
    ]  # Replace later
    descriptions = []
    for x in record.findall(".//dc:description", namespace):
        if x.text is not None:
            descriptions.append(Description(dsDescriptionValue=x.text))
    subjects = []
    for x in record.findall(".//dc:subject", namespace):
        if x.text is not None:
            subjects.append(x.text)

    return Dataset(
        title=title,
        authors=authors,
        contacts=contacts,
        description=descriptions,
        subjects=subjects,
    )


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


# Dataverse metadata block types


def compound(values: List, type_name: str, subtype_names: List[str]) -> dict:
    result: Dict[str, Any] = {
        "value": [],
        "typeClass": "compound",
        "multiple": True,
        "typeName": type_name,
    }

    for v in values:
        result["value"].append(
            {
                subtype: primitive(getattr(v, subtype), subtype)
                for subtype in subtype_names
                if getattr(v, subtype) is not None
            }
        )

    return result


def controlled(values: List[str], type_name: str) -> dict:
    result = {
        "value": values,
        "typeClass": "controlledVocabulary",
        "multiple": True,
        "typeName": type_name,
    }

    return result


def primitive(value: str, type_name: str) -> dict:
    result = {
        "value": value,
        "typeClass": "primitive",
        "multiple": False,
        "typeName": type_name,
    }

    return result
