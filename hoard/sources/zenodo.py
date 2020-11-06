from datetime import datetime
from typing import Any, Dict, Iterator

import pycountry  # type: ignore
import structlog  # type: ignore
import xml.etree.ElementTree as ET

from hoard.client import OAIClient
from hoard.models import (
    Author,
    Contact,
    Contributor,
    Dataset,
    Description,
    Keyword,
    OtherId,
    Producer,
    Publication,
)

logger = structlog.get_logger()

namespace = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "datacite": "http://schema.datacite.org/oai/oai-1.0/",
    "datacite3": "http://datacite.org/schema/kernel-3",
}


class Zenodo:
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
                    dataset = create_from_zenodo_datacite_xml(record, self.client)
                    return dataset
                except TypeError as ex:
                    id_elem = parsed_record.find(".//oai:identifier", namespace)
                    if id_elem is not None:
                        rec_id = id_elem.text
                    logger.info(f"Error with {rec_id}: {str(ex)}")


def create_from_zenodo_datacite_xml(data: str, client: OAIClient) -> Dataset:
    kwargs: Dict[str, Any] = {}
    record = ET.fromstring(data)
    titles = record.findall(".//datacite3:title", namespace)
    # how to deal with multiple titles?
    for title in titles:
        kwargs["title"] = title.text
    creators = record.findall(".//datacite3:creator", namespace)
    for creator in creators:
        creatorName = get_child_elem_text(creator, "creatorName")
        creatorAffiliation = get_child_elem_text(creator, "affiliation")
        creatorNameIdentifier = get_child_elem_text(creator, "nameIdentifier")
        kwargs.setdefault("authors", []).append(
            Author(
                authorName=creatorName,
                authorAffiliation=creatorAffiliation,
                authorIdentifier=creatorNameIdentifier,
            )
        )
    kwargs["contacts"] = [
        Contact(datasetContactName="!!!!!!", datasetContactEmail="!!!!!!",)
    ]
    descriptions = record.findall(".//datacite3:description", namespace)
    for description in [
        d
        for d in descriptions
        if "descriptionType" in d.attrib and d.attrib["descriptionType"] == "Abstract"
    ]:
        if description.text is not None:
            kwargs.setdefault("description", []).append(
                Description(dsDescriptionValue=description.text)
            )
    subjects = record.findall(".//datacite3:subject", namespace)
    for subject in subjects:
        kwargs.setdefault("keywords", []).append(Keyword(keywordValue=subject.text))
    dates = record.findall(".//datacite3:date", namespace)
    for date in [
        d for d in dates if "dateType" in d.attrib and d.attrib["dateType"] == "Issued"
    ]:
        if date.text is not None:
            try:
                datetime.strptime(date.text, "%Y-%m-%d")
                kwargs["distributionDate"] = date.text
            except ValueError:
                pass
    identifier = record.find(".//datacite3:identifier", namespace)
    if identifier is not None:
        kwargs["alternativeURL"] = identifier.text
    alternate_ids = record.findall(".//datacite3:alternateIdentifier", namespace)
    for alternate_id in alternate_ids:
        kwargs.setdefault("otherIds", []).append(
            OtherId(otherIdValue=alternate_id.text)
        )
    resource_types = record.findall(".//datacite3:resourceType", namespace)
    for resource_type in resource_types:
        if resource_type.text is not None:
            kwargs.setdefault("kindOfData", []).append(resource_type.text)
        if resource_type.attrib["resourceTypeGeneral"] is not None:
            kwargs.setdefault("kindOfData", []).append(
                resource_type.attrib["resourceTypeGeneral"]
            )
    contributors = record.findall(".//datacite3:contributor", namespace)
    for contributor in contributors:
        contributorName = get_child_elem_text(contributor, "contributorName")
        contributorType = get_child_elem_text(contributor, "contributorType")
        kwargs.setdefault("contributors", []).append(
            Contributor(
                contributorName=contributorName, contributorType=contributorType
            )
        )
    publishers = record.findall(".//datacite3:publisher", namespace)
    for publisher in [p for p in publishers if p is not None]:
        kwargs.setdefault("producers", []).append(Producer(producerName=publisher.text))
    related_ids = record.findall(".//datacite3:relatedIdentifier", namespace)
    for related_id in [
        r
        for r in related_ids
        if "relationType" in r.attrib and r.attrib["relationType"] == "IsSupplementTo"
    ]:
        publicationIDNumber = None
        publicationIDType = None
        if related_id.text is not None:
            publicationIDNumber = related_id.text
        if "relatedIdentifierType" in related_id.attrib:
            publicationIDType = related_id.attrib["relatedIdentifierType"]
        kwargs.setdefault("publications", []).append(
            Publication(
                publicationIDNumber=publicationIDNumber,
                publicationIDType=publicationIDType,
            )
        )
    languages = record.findall(".//datacite3:language", namespace)
    for language in [x for x in languages if x is not None]:
        if language.text is not None:
            lang_value = pycountry.languages.get(alpha_2=language.text[:2])
            if lang_value != "":
                kwargs.setdefault("language", []).append(lang_value.name)
    rights_list = record.findall(".//datacite3:rights", namespace)
    # workaround until we figure out parsing
    all_rights = ""
    for rights in rights_list:
        if rights.text is not None:
            if all_rights != "":
                all_rights += f". {rights.text}"
            else:
                all_rights = rights.text
    if all_rights != "":
        kwargs["license"] = all_rights
        kwargs["termsOfUse"] = all_rights
    kwargs["subjects"] = ["!!!!!!"]
    if "description" not in kwargs:
        kwargs["description"] = [Description(dsDescriptionValue=kwargs["title"])]
    return Dataset(**kwargs)


def get_child_elem_text(child_elem, child_elem_name):
    child_elem = child_elem.find(f"datacite3:{child_elem_name}", namespace)
    if child_elem is not None:
        child_elem = child_elem.text
    return child_elem
