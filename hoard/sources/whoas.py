from datetime import datetime
from typing import Any, Dict, Iterator
from urllib.parse import urlparse

import pycountry  # type: ignore
import structlog  # type: ignore
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

logger = structlog.get_logger()

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
                try:
                    dataset = create_from_whoas_dim_xml(record, self.client)
                    return dataset
                except TypeError as ex:
                    id_elem = parsed_record.find(".//oai:identifier", namespace)
                    if id_elem is not None:
                        rec_id = id_elem.text
                    logger.info(f"Error with {rec_id}: {str(ex)}")


def create_from_whoas_dim_xml(data: str, client: OAIClient) -> Dataset:
    kwargs: Dict[str, Any] = {}
    record = ET.fromstring(data)
    fields = record.findall(".//dim:field", namespace)
    kwargs["contacts"] = [
        Contact(
            datasetContactName="Woods Hole Open Access Server",
            datasetContactEmail="whoas@whoi.edu",
        )
    ]
    notesText = ""
    for field in fields:
        if field.attrib["element"] == "title" and "qualifier" not in field.attrib:
            kwargs["title"] = field.text
        if (
            field.attrib["element"] == "contributor"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "author"
        ):
            if field.text is not None:
                kwargs.setdefault("authors", []).append(
                    Author(authorName=field.text, authorAffiliation="Woods Hole")
                )
        if (
            field.attrib["element"] == "description"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "abstract"
        ):
            if field.text is not None:
                kwargs.setdefault("description", []).append(
                    Description(dsDescriptionValue=field.text)
                )
        if field.attrib["element"] == "subject":
            kwargs.setdefault("keywords", []).append(Keyword(keywordValue=field.text))
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
            and field.text is not None
        ):
            try:
                datetime.strptime(field.text, "%Y-%m-%d")
                kwargs["distributionDate"] = field.text
            except ValueError:
                pass
        if field.attrib["element"] == "publisher":
            kwargs.setdefault("distributors", []).append(
                Distributor(distributorName=field.text)
            )
        if (
            field.attrib["element"] == "description"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "sponsorship"
        ):
            kwargs.setdefault("grantNumbers", []).append(
                GrantNumber(grantNumberInformation=field.text)
            )
        if field.attrib["element"] == "description" and "qualifier" not in field.attrib:
            if field.text is not None and notesText == "":
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
                    kwargs.setdefault("language", []).append(lang_value.name)
        if field.attrib["element"] == "identifier":
            kwargs.setdefault("otherIds", []).append(OtherId(otherIdValue=field.text))
        if (
            field.attrib["element"] == "coverage"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "spatial"
        ):
            kwargs["productionPlace"] = field.text
        if field.attrib["element"] == "relation" and "qualifier" not in field.attrib:
            kwargs.setdefault("publications", []).append(
                Publication(publicationCitation=field.text)
            )
        if (
            field.attrib["element"] == "relation"
            and "qualifier" in field.attrib
            and field.attrib["qualifier"] == "ispartof"
        ):
            if field.text is not None and field.text.startswith(
                "https://hdl.handle.net/"
            ):
                series_args = {"seriesInformation": field.text}
                parsed_url = urlparse(field.text)
                id = f"oai:darchive.mblwhoilibrary.org:{parsed_url.path[1:]}"
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
                time_kwargs = {}
                try:
                    datetime.strptime(start, "%Y-%m-%d")
                    time_kwargs["timePeriodCoveredStart"] = start
                except ValueError:
                    pass
                try:
                    datetime.strptime(end, "%Y-%m-%d")
                    time_kwargs["timePeriodCoveredEnd"] = end
                except ValueError:
                    pass
                kwargs.setdefault("timePeriodsCovered", []).append(
                    TimePeriodCovered(**time_kwargs)
                )
        if field.attrib["element"] == "rights" and "qualifier" not in field.attrib:
            kwargs["license"] = field.text
            kwargs["termsOfUse"] = field.text

    kwargs["subjects"] = ["Earth and Environmental Sciences"]
    if "description" not in kwargs:
        kwargs["description"] = [Description(dsDescriptionValue=kwargs["title"])]
    if notesText != "":
        kwargs["notesText"] = notesText
    return Dataset(**kwargs)
