from typing import Any, Dict, List, Optional

import attr


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
        return attr.asdict(self)

    def dv_format(self) -> dict:
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


def create_from_dict(data: dict) -> Dataset:
    title = data["title"]
    author = Author(
        authorName=data["authorName"], authorAffiliation=data["authorAffiliation"]
    )
    contact = Contact(
        datasetContactName=data["contactName"], datasetContactEmail=data["contactEmail"]
    )
    description = Description(dsDescriptionValue=data["description"])
    return Dataset(
        title=title,
        authors=[author],
        contacts=[contact],
        description=[description],
        subjects=data["subjects"],
    )


# Metadata block types


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
