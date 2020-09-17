from typing import Any, Dict, List, Optional

import attr


@attr.s(auto_attribs=True)
class Author:
    authorName: str
    authorAffiliation: str
    authorIdentifierScheme: Optional[str] = None
    authorIdentifier: Optional[str] = None


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
class Keyword:
    keywordValue: Optional[str] = None


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
    alternativeURL: Optional[str] = None
    contributors: Optional[List[Contributor]] = None
    distributionDate: Optional[str] = None
    distributors: Optional[List[Distributor]] = None
    grantNumbers: Optional[List[GrantNumber]] = None
    keywords: Optional[List[Keyword]] = None
    kindOfData: Optional[List[str]] = None
    language: Optional[List[str]] = None
    notesText: Optional[str] = None
    otherIds: Optional[List[OtherId]] = None
    producers: Optional[List[Producer]] = None
    productionPlace: Optional[str] = None
    publications: Optional[List[Publication]] = None
    series: Optional[Series] = None
    timePeriodsCovered: Optional[List[TimePeriodCovered]] = None
    license: Optional[str] = None
    termsOfUse: Optional[str] = None

    def asdict(self) -> dict:
        fields = [primitive(self.title, "title")]
        if self.alternativeURL is not None:
            fields.append(primitive(self.alternativeURL, "alternativeURL"))
        authors = compound(
            self.authors,
            "author",
            [
                "authorName",
                "authorAffiliation",
                "authorIdentifierScheme",
                "authorIdentifier",
            ],
        )
        for author in authors["value"]:
            if "authorIdentifierScheme" in author:
                author["authorIdentifierScheme"]["typeClass"] = "controlledVocabulary"
        fields.append(authors)
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
            contributors = compound(
                self.contributors,
                "contributor",
                ["contributorName", "contributorType"],
            )
            for contributor in contributors["value"]:
                contributor["contributorType"]["typeClass"] = "controlledVocabulary"
            fields.append(contributors)
        fields.append(
            compound(
                self.description,
                "dsDescription",
                ["dsDescriptionValue", "dsDescriptionDate"],
            )
        )
        if self.distributionDate is not None:
            fields.append(primitive(self.distributionDate, "distributionDate"))
        if self.distributors is not None:
            fields.append(
                compound(
                    self.distributors,
                    "distributor",
                    ["distributorName", "distributorURL"],
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
        if self.keywords is not None:
            fields.append(compound(self.keywords, "keyword", ["keywordValue"]))
        if self.kindOfData is not None:
            fields.append(
                {
                    "typeName": "kindOfData",
                    "multiple": True,
                    "typeClass": "primitive",
                    "value": self.kindOfData,
                }
            )
        if self.language is not None:
            fields.append(controlled(self.language, "language"))
        if self.notesText is not None:
            fields.append(primitive(self.notesText, "notesText"))
        if self.otherIds is not None:
            fields.append(
                compound(self.otherIds, "otherId", ["otherIdValue", "otherIdAgency"],)
            )
        if self.producers is not None:
            fields.append(
                compound(self.producers, "producer", ["producerName", "producerURL"],)
            )
        if self.productionPlace is not None:
            fields.append(primitive(self.productionPlace, "productionPlace"))
        if self.publications is not None:
            publications = compound(
                self.publications,
                "publication",
                [
                    "publicationCitation",
                    "publicationIDNumber",
                    "publicationIDType",
                    "publicationURL",
                ],
            )
            for publication in publications["value"]:
                publication["publicationIDType"]["typeClass"] = "controlledVocabulary"
            fields.append(publications)
        if self.series is not None:
            fields.append(
                {
                    "typeName": "series",
                    "multiple": False,
                    "typeClass": "compound",
                    "value": {
                        "seriesName": {
                            "multiple": False,
                            "typeClass": "primitive",
                            "typeName": "seriesName",
                            "value": self.series.seriesName,
                        },
                        "seriesInformation": {
                            "multiple": False,
                            "typeClass": "primitive",
                            "typeName": "seriesInformation",
                            "value": self.series.seriesInformation,
                        },
                    },
                }
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
        result: Dict[str, Any] = {
            "datasetVersion": {
                "metadataBlocks": {
                    "citation": {"displayName": "Citation Metadata", "fields": fields}
                }
            }
        }
        if self.license is not None:
            result["datasetVersion"]["license"] = self.license
        if self.termsOfUse is not None:
            result["datasetVersion"]["termsOfUse"] = self.termsOfUse
        return result


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
