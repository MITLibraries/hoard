from typing import Any, Dict, List, Optional, Union

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
    grantNumberInformation: Optional[str] = None


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
        fields: List[Optional[Dict[str, Any]]] = [primitive(self.title, "title")]

        fields.append(primitive(self.alternativeURL, "alternativeURL"))

        fields.append(
            compound(
                self.authors,
                "author",
                [
                    "authorName",
                    "authorAffiliation",
                    "authorIdentifierScheme",
                    "authorIdentifier",
                ],
                controlled_subfield="authorIdentifierScheme",
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
            compound(
                self.contributors,
                "contributor",
                ["contributorName", "contributorType"],
                controlled_subfield="contributorType",
            )
        )

        fields.append(
            compound(
                self.description,
                "dsDescription",
                ["dsDescriptionValue", "dsDescriptionDate"],
            )
        )

        fields.append(primitive(self.distributionDate, "distributionDate"))

        fields.append(
            compound(
                self.distributors, "distributor", ["distributorName", "distributorURL"],
            )
        )

        fields.append(
            compound(
                self.grantNumbers,
                "grantNumber",
                ["grantNumberValue", "grantNumberAgency"],
            )
        )
        fields.append(compound(self.keywords, "keyword", ["keywordValue"]))

        fields.append(primitive(self.kindOfData, "kindOfData", multiple=True))

        fields.append(controlled(self.language, "language"))

        fields.append(primitive(self.notesText, "notesText"))

        fields.append(
            compound(self.otherIds, "otherId", ["otherIdValue", "otherIdAgency"],)
        )

        fields.append(
            compound(self.producers, "producer", ["producerName", "producerURL"],)
        )

        fields.append(primitive(self.productionPlace, "productionPlace"))

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
                controlled_subfield="publicationIDType",
            )
        )

        if self.series is not None:
            series: Dict[str, Any] = {
                "typeName": "series",
                "multiple": False,
                "typeClass": "compound",
                "value": {},
            }
            if self.series.seriesName:
                series["value"]["seriesName"] = primitive(
                    self.series.seriesName, "seriesName"
                )
            if self.series.seriesInformation:
                series["value"]["seriesInformation"] = primitive(
                    self.series.seriesInformation, "seriesInformation"
                )
            fields.append(series)

        fields.append(controlled(self.subjects, "subject"))

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
                    "citation": {
                        "displayName": "Citation Metadata",
                        "fields": list(filter(None, fields)),
                    }
                }
            }
        }

        if self.license is not None:
            result["datasetVersion"]["license"] = self.license
        if self.termsOfUse is not None:
            result["datasetVersion"]["termsOfUse"] = self.termsOfUse

        return result


# Dataverse metadata block types


def compound(
    values: Optional[List],
    type_name: str,
    subtype_names: List[str],
    controlled_subfield: Optional[str] = None,
) -> Optional[dict]:
    if not values:
        return None
    result: Dict[str, Any] = {
        "value": [],
        "typeClass": "compound",
        "multiple": True,
        "typeName": type_name,
    }
    for i, v in enumerate(values):
        result["value"].append(
            {
                subtype: primitive(getattr(v, subtype), subtype)
                for subtype in subtype_names
                if getattr(v, subtype) is not None
            }
        )
        if (
            controlled_subfield is not None
            and controlled_subfield in result["value"][i]
        ):
            result["value"][i][controlled_subfield][
                "typeClass"
            ] = "controlledVocabulary"

    return result


def controlled(values: Optional[List[str]], type_name: str) -> Optional[dict]:
    if not values:
        return None
    result = {
        "value": values,
        "typeClass": "controlledVocabulary",
        "multiple": True,
        "typeName": type_name,
    }

    return result


def primitive(
    value: Optional[Union[List, str]], type_name: str, multiple: bool = False
) -> Optional[dict]:
    if not value:
        return None
    result = {
        "value": value,
        "typeClass": "primitive",
        "multiple": multiple,
        "typeName": type_name,
    }

    return result
