from typing import Any, Dict, Iterator

import xml.etree.ElementTree as ET

from hoard.client import OAIClient
from hoard.models import (
    Author,
    Contact,
    Dataset,
    Description,
    Distributor,
    GrantNumber,
    Keyword,
    OtherId,
    Publication,
    Series,
    TimePeriodCovered,
)


class WHOAS:
    def __init__(self, client: OAIClient) -> None:
        self.client = client

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        record = next(self.client)
        dataset = create_from_whoas_dim_xml(record)
        return dataset


def create_from_whoas_dim_xml(data: str) -> Dataset:
    kwargs: Dict[str, Any] = {}
    record = ET.fromstring(data)
    namespace = {
        "oai": "http://www.openarchives.org/OAI/2.0/",
        "dim": "http://www.dspace.org/xmlns/dspace/dim",
    }
    fields = record.findall(".//dim:field", namespace)
    authors = []
    contacts = [
        Contact(
            datasetContactName="NAME, FAKE",
            datasetContactEmail="FAKE_EMAIL@FAKE_DOMAIN.EDU",
        )
    ]
    descriptions = []
    subjects = []
    distributors = []
    grantNumbers = []
    keywords = []
    kindOfData = []
    otherIds = []
    publications = []
    timePeriodsCovered = []
    for field in fields:
        if field.attrib["element"] == "title" and "qualifier" not in field.attrib:
            kwargs["title"] = field.text
        if (
            field.attrib["element"] == "contributor"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "author"
        ):
            if field.text is not None:
                authors.append(
                    Author(authorName=field.text, authorAffiliation="Woods Hole")
                )
            else:
                authors.append(Author(authorName="", authorAffiliation=""))
        if (
            field.attrib["element"] == "description"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "abstract"
        ):
            if field.text is not None:
                descriptions.append(Description(dsDescriptionValue=field.text))
            else:
                descriptions.append(Description(dsDescriptionValue=""))
        if field.attrib["element"] == "subject":
            subjects.append(field.text)
            keywords.append(Keyword(keywordValue=field.text))
        if (
            field.attrib["element"] == "identifier"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "uri"
        ):
            kwargs["alternativeURL"] = field.text
        if (
            field.attrib["element"] == "date"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "issued"
        ):
            kwargs["distributionDate"] = field.text
        if field.attrib["element"] == "publisher":
            distributors.append(Distributor(distributorName=field.text))
        if (
            field.attrib["element"] == "description"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "sponsorship"
        ):
            grantNumbers.append(
                GrantNumber(grantNumberValue=field.text, grantNumberAgency=field.text)
            )
        if field.attrib["element"] == "description" and "qualifier" not in field.attrib:
            kindOfData.append(field.text)
        if (
            field.attrib["element"] == "language"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "iso"
        ):
            kwargs["language"] = field.text
        if field.attrib["element"] == "identifier":
            otherIds.append(OtherId(otherIdValue=field.text))
        if (
            field.attrib["element"] == "coverage"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "spacial"
        ):
            kwargs["productionPlace"] = field.text
        if field.attrib["element"] == "relation" and "qualifier" not in field.attrib:
            publications.append(Publication(publicationCitation=field.text))
        if (
            field.attrib["element"] == "relation"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "ispartof"
        ):
            kwargs["series"] = Series(seriesInformation=field.text)
        if (
            field.attrib["element"] == "coverage"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "temporal"
        ):
            if field.text is not None and " - " in field.text:
                start = field.text[: field.text.index(" - ")]
                end = field.text[field.text.index(" - ") + 3 : field.text.index("(UTC")]
                timePeriodsCovered.append(
                    TimePeriodCovered(
                        timePeriodCoveredStart=start, timePeriodCoveredEnd=end,
                    )
                )
            if field.attrib["element"] == "rights" and "qualifier" not in field.attrib:
                kwargs["license"] = field.text
                kwargs["termsOfUse"] = field.text

    kwargs["authors"] = authors
    kwargs["contacts"] = contacts
    kwargs["description"] = descriptions
    kwargs["subjects"] = subjects
    kwargs["distributors"] = distributors
    kwargs["grantNumbers"] = grantNumbers
    kwargs["keywords"] = keywords
    kwargs["kindOfData"] = kindOfData
    kwargs["otherIds"] = otherIds
    kwargs["publications"] = publications
    return Dataset(**kwargs)
