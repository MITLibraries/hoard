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
class Contributor:
    contributorName: Optional[str] = None
    contributorType: Optional[str] = None


@attr.s(auto_attribs=True)
class DatasetVersion:
    license: Optional[str] = None
    termsOfUse: Optional[str] = None


@attr.s(auto_attribs=True)
class Description:
    dsDescriptionValue: str
    dsDescriptionDate: Optional[str] = None


@attr.s(auto_attribs=True)
class Distributor:
    distributorName: Optional[str] = None
    distributorURL: Optional[str] = None


@attr.s(auto_attribs=True)
class GrantNumber:
    grantNumberValue: Optional[str] = None
    grantNumberAgency: Optional[str] = None


@attr.s(auto_attribs=True)
class OtherId:
    otherIdValue: Optional[str] = None
    otherIdAgency: Optional[str] = None


@attr.s(auto_attribs=True)
class Producer:
    producerName: Optional[str] = None
    producerURL: Optional[str] = None


@attr.s(auto_attribs=True)
class Publication:
    publicationCitation: Optional[str] = None
    publicationIDNumber: Optional[str] = None
    publicationIDType: Optional[str] = None
    publicationURL: Optional[str] = None


@attr.s(auto_attribs=True)
class Series:
    seriesName: Optional[str] = None
    seriesInformation: Optional[str] = None


@attr.s(auto_attribs=True)
class TimePeriodCovered:
    timePeriodCoveredStart: Optional[str] = None
    timePeriodCoveredEnd: Optional[str] = None


@attr.s(auto_attribs=True)
class Dataset:
    authors: List[Author]
    contacts: List[Contact]
    description: List[Description]
    subjects: List[str]
    title: str
    alternateUrl: Optional[str] = None
    contributors: Optional[List[Contributor]] = None
    distributionDate: Optional[str] = None
    distributors: Optional[List[Distributor]] = None
    grantNumbers: Optional[List[GrantNumber]] = None
    keywordValue: Optional[str] = None
    kindOfData: Optional[str] = None
    language: Optional[str] = None
    notesText: Optional[str] = None
    otherIds: Optional[List[OtherId]] = None
    producers: Optional[List[Producer]] = None
    productionPlace: Optional[str] = None
    publications: Optional[List[Publication]] = None
    series: Optional[List[Series]] = None
    timePeriodsCovered: Optional[List[TimePeriodCovered]] = None

    def asdict(self) -> dict:
        fields = [primitive(self.title, "title")]
        if self.alternateUrl is not None:
            fields = [primitive(self.alternateUrl, "alternateUrl")]
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
        if self.contributors is not None:
            fields.append(
                compound(
                    self.contributors,
                    "contributor",
                    ["contributorName", "contributorType"],
                )
            )
        fields.append(
            compound(self.description, "dsDescription", ["dsDescriptionValue"])
        )
        if self.distributionDate is not None:
            fields = [primitive(self.distributionDate, "distributionDate")]
        if self.distributors is not None:
            fields.append(
                compound(
                    self.distributors,
                    "distributor",
                    ["distributorName", "distributorType"],
                )
            )
        if self.grantNumbers is not None:
            fields.append(
                compound(
                    self.grantNumbers,
                    "grantNumber",
                    ["grantNumberValue", "grantNumberAgency"],
                )
            )
        if self.keywordValue is not None:
            fields = [primitive(self.keywordValue, "keywordValue")]
        if self.kindOfData is not None:
            fields = [primitive(self.kindOfData, "kindOfData")]
        if self.language is not None:
            fields = [primitive(self.language, "language")]
        if self.notesText is not None:
            fields = [primitive(self.notesText, "notesText")]
        if self.otherIds is not None:
            fields.append(
                compound(self.otherIds, "otherId", ["otherIdValue", "otherIdAgency"],)
            )
        if self.producers is not None:
            fields.append(
                compound(self.producers, "producer", ["producerName", "producerURL"],)
            )
        if self.productionPlace is not None:
            fields = [primitive(self.productionPlace, "productionPlace")]
        if self.publications is not None:
            fields.append(
                compound(
                    self.publications,
                    "publication",
                    [
                        "publicationCitation",
                        "publicationIDNumber",
                        "publicationIDType",
                        "publicationURL",
                    ],
                )
            )
        if self.series is not None:
            fields.append(
                compound(self.series, "series", ["seriesName", "seriesInformation"],)
            )
        fields.append(controlled(self.subjects, "subject"))
        if self.timePeriodsCovered is not None:
            fields.append(
                compound(
                    self.timePeriodsCovered,
                    "timePeriodCovered",
                    ["timePeriodCoveredStart", "timePeriodCoveredEnd"],
                )
            )

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
