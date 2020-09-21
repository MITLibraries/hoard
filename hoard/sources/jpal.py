from bs4 import BeautifulSoup  # type: ignore
import requests
from typing import Any, Dict, Iterator, Optional


from hoard.client import OAIClient
from hoard.models import (
    Author,
    Contact,
    Contributor,
    Dataset,
    Description,
    Distributor,
    GrantNumber,
    Keyword,
    OtherId,
    Producer,
    Publication,
    Series,
    TimePeriodCovered,
)


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
    kwargs: Dict[str, Any] = {}

    # Dataset fields
    kwargs["alternativeURL"] = data.get("persistentUrl")
    kwargs["distributionDate"] = data.get("publicationDate")
    kwargs["distributors"] = [
        Distributor(
            distributorName="The Abdul Latif Jameel Poverty Action Lab Dataverse",
            distributorURL="https://dataverse.harvard.edu/dataverse/jpal",
        )
    ]
    kwargs["license"] = data["datasetVersion"].get("license")
    kwargs["termsOfUse"] = data["datasetVersion"].get("termsOfUse")

    # Citation fields
    fields = data["datasetVersion"]["metadataBlocks"]["citation"]["fields"]

    for field in fields:
        if field["typeName"] == "author":
            kwargs["authors"] = [
                Author(
                    authorAffiliation=v["authorAffiliation"]["value"],
                    authorIdentifier=get_optional_value(v, "authorIdentifier"),
                    authorIdentifierScheme=get_optional_value(
                        v, "authorIdentifierScheme"
                    ),
                    authorName=v["authorName"]["value"],
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "datasetContact":
            kwargs["contacts"] = [
                Contact(
                    datasetContactAffiliation=get_optional_value(
                        v, "datasetContactAffiliation"
                    ),
                    datasetContactEmail=v["datasetContactEmail"]["value"],
                    datasetContactName=v["datasetContactName"]["value"],
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "contributor":
            kwargs["contributors"] = [
                Contributor(
                    contributorName=get_optional_value(v, "contributorName"),
                    contributorType=get_optional_value(v, "contributorType"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "dsDescription":
            kwargs["description"] = [
                Description(
                    dsDescriptionDate=get_optional_value(v, "dsDescriptionDate"),
                    dsDescriptionValue=v["dsDescriptionValue"]["value"],
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "distributor":
            kwargs["distributors"].extend(
                [
                    Distributor(
                        distributorName=get_optional_value(v, "distributorName"),
                        distributorURL=get_optional_value(v, "distributorURL"),
                    )
                    for v in field["value"]
                ]
            )

        elif field["typeName"] == "grantNumber":
            kwargs["grantNumbers"] = [
                GrantNumber(
                    grantNumberAgency=get_optional_value(v, "grantNumberAgency"),
                    grantNumberValue=get_optional_value(v, "grantNumberValue"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "keyword":
            kwargs["keywords"] = [
                Keyword(keywordValue=get_optional_value(v, "keywordValue"),)
                for v in field["value"]
            ]

        elif field["typeName"] == "kindOfData":
            kwargs["kindOfData"] = field["value"]

        elif field["typeName"] == "language":
            kwargs["language"] = field["value"]

        elif field["typeName"] == "notesText":
            kwargs["notesText"] = field["value"]

        elif field["typeName"] == "otherId":
            kwargs["otherIds"] = [
                OtherId(
                    otherIdAgency=get_optional_value(v, "otherIdAgency"),
                    otherIdValue=get_optional_value(v, "otherIdValue"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "producer":
            kwargs["producers"] = [
                Producer(
                    producerName=get_optional_value(v, "producerName"),
                    producerURL=get_optional_value(v, "producerURL"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "productionPlace":
            kwargs["productionPlace"] = field["value"]

        elif field["typeName"] == "publication":
            kwargs["publications"] = [
                Publication(
                    publicationCitation=get_optional_value(v, "publicationCitation"),
                    publicationIDNumber=get_optional_value(v, "publicationIDNumber"),
                    publicationIDType=get_optional_value(v, "publicationIDType"),
                    publicationURL=get_optional_value(v, "publicationURL"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "series":
            kwargs["series"] = Series(
                seriesName=get_optional_value(field["value"], "seriesName"),
                seriesInformation=get_optional_value(
                    field["value"], "seriesInformation"
                ),
            )

        elif field["typeName"] == "subject":
            kwargs["subjects"] = field["value"]

        elif field["typeName"] == "timePeriodCovered":
            kwargs["timePeriodsCovered"] = [
                TimePeriodCovered(
                    timePeriodCoveredStart=get_optional_value(
                        v, "timePeriodCoveredStart"
                    ),
                    timePeriodCoveredEnd=get_optional_value(v, "timePeriodCoveredEnd"),
                )
                for v in field["value"]
            ]

        elif field["typeName"] == "title":
            kwargs["title"] = field["value"]

    return Dataset(**kwargs)


def get_optional_value(d: dict, k: str) -> Optional[str]:
    if d.get(k) is not None:
        return d[k]["value"]
    else:
        return None
