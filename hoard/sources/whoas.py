from typing import Any, Dict, Iterator

import pycountry  # type: ignore
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


namespace = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "dim": "http://www.dspace.org/xmlns/dspace/dim",
}


class WHOAS:
    def __init__(self, client: OAIClient) -> None:
        self.client = client

    def __iter__(self) -> Iterator[Dataset]:
        return self

    def __next__(self) -> Dataset:
        while True:
            record = next(self.client)
            parsed_record = ET.fromstring(record)
            if parsed_record.find(".//oai:error", namespace) is not None:
                continue
            else:
                dataset = create_from_whoas_dim_xml(record, self.client)
            return dataset


def create_from_whoas_dim_xml(data: str, client: OAIClient) -> Dataset:
    kwargs: Dict[str, Any] = {}
    record = ET.fromstring(data)
    fields = record.findall(".//dim:field", namespace)
    authors = []
    contacts = [
        Contact(
            datasetContactName="NAME, FAKE",
            datasetContactEmail="FAKE_EMAIL@EXAMPLE.COM",
        )
    ]
    descriptions = []
    distributors = []
    grantNumbers = []
    keywords = []
    languages = []
    notesText = None
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
        if (
            field.attrib["element"] == "description"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "abstract"
        ):
            if field.text is not None:
                descriptions.append(Description(dsDescriptionValue=field.text))
        if field.attrib["element"] == "subject":
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
            if notesText is None:
                notesText = field.text
            else:
                notesText += f" {field.text}"
        if (
            field.attrib["element"] == "language"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "iso"
        ):
            if field.text is not None:
                lang_value = pycountry.languages.get(alpha_2=field.text[:2])
                if lang_value != "":
                    languages.append(lang_value.name)
        if field.attrib["element"] == "identifier":
            otherIds.append(OtherId(otherIdValue=field.text))
        if (
            field.attrib["element"] == "coverage"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "spatial"
        ):
            kwargs["productionPlace"] = field.text
        if field.attrib["element"] == "relation" and "qualifier" not in field.attrib:
            publications.append(Publication(publicationCitation=field.text))
        if (
            field.attrib["element"] == "relation"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "ispartof"
        ):
            if field.text is not None and field.text.startswith(
                "https://hdl.handle.net/"
            ):
                series_args = {"seriesInformation": field.text}
                id = f"oai:darchive.mblwhoilibrary.org:{field.text[23:]}"
                series_name = client.get_record_title(id)
                series_args["seriesName"] = series_name
                kwargs["series"] = Series(**series_args)
        if (
            field.attrib["element"] == "coverage"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "temporal"
        ):
            if field.text is not None and " - " in field.text:
                dates = field.text.split(" - ")
                start = dates[0]
                end = dates[1].rstrip(" (UTC)")
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
    kwargs["subjects"] = ["Earth and Environmental Sciences"]
    kwargs["distributors"] = distributors
    kwargs["grantNumbers"] = grantNumbers
    kwargs["keywords"] = keywords
    kwargs["language"] = languages
    kwargs["notesText"] = notesText
    kwargs["otherIds"] = otherIds
    kwargs["publications"] = publications
    kwargs["timePeriodsCovered"] = timePeriodsCovered
    return Dataset(**kwargs)
