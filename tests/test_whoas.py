import requests_mock
from unittest.mock import MagicMock

from hoard.client import OAIClient
from hoard.models import (
    Author,
    Contact,
    Description,
    Distributor,
    GrantNumber,
    Keyword,
    OtherId,
    Publication,
    Series,
    TimePeriodCovered,
)
from hoard.sources.whoas import create_from_whoas_dim_xml, WHOAS


def test_create_whoas_dim_xml(whoas_oai_server, dspace_oai_xml_series_name_record):
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/oai?verb=GetRecord&metadataPrefix=dim"
            "&identifier=oai%3Adarchive.mblwhoilibrary.org:1912/6867",
            text=dspace_oai_xml_series_name_record,
        )
        client = OAIClient("http+mock://example.com/oai", "dim", "Test_Collection")
        title = (
            "Animals on the Move and Deep‐Sea Vents: Dataset for Spherical Display "
            "Systems"
        )
        authors = [
            Author(
                authorName="Beaulieu, Stace E.",
                authorAffiliation="Woods Hole",
                authorIdentifierScheme=None,
                authorIdentifier=None,
            ),
            Author(
                authorName="Brickley, Annette",
                authorAffiliation="Woods Hole",
                authorIdentifierScheme=None,
                authorIdentifier=None,
            ),
        ]
        contacts = [
            Contact(
                datasetContactName="NAME, FAKE",
                datasetContactEmail="FAKE_EMAIL@EXAMPLE.COM",
            )
        ]
        description = [
            Description(
                dsDescriptionValue="This educational package was developed.",
                dsDescriptionDate=None,
            ),
            Description(dsDescriptionValue="Sample abstract", dsDescriptionDate=None,),
        ]
        distributors = [Distributor(distributorName="Esteemed Publishing Conglomerate")]
        grantNumbers = [
            GrantNumber(
                grantNumberValue="Funding for this educational package.",
                grantNumberAgency="Funding for this educational package.",
            )
        ]
        keywords = [
            Keyword(keywordValue="Migration"),
            Keyword(keywordValue="Larval dispersal"),
        ]
        notesText = (
            "This zipped file contains educational materials. "
            "This educational package is Copyright ©2019 Woods"
            " Hole Oceanographic Institution."
        )
        otherIds = [
            OtherId(
                otherIdValue="https://hdl.handle.net/1912/2368", otherIdAgency=None
            ),
            OtherId(otherIdValue="10.26025/8ke9-av98", otherIdAgency=None),
        ]
        publications = [Publication(publicationCitation="Associated publication")]
        series = Series(
            seriesName="Series Title",
            seriesInformation="https://hdl.handle.net/1912/6867",
        )

        timePeriodsCovered = [
            TimePeriodCovered(
                timePeriodCoveredStart="2019-06-04", timePeriodCoveredEnd="2019-06-04",
            )
        ]
        subjects = ["Earth and Environmental Sciences"]
        dataset = create_from_whoas_dim_xml(whoas_oai_server[0], client)
        assert dataset.title == title
        assert dataset.authors == authors
        assert dataset.contacts == contacts
        assert dataset.description == description
        assert dataset.subjects == subjects

        dataset = create_from_whoas_dim_xml(whoas_oai_server[1], client)
        assert dataset.title == title
        assert dataset.authors == authors
        assert dataset.contacts == contacts
        assert dataset.description == description
        assert dataset.subjects == subjects
        assert dataset.distributors == distributors
        assert dataset.grantNumbers == grantNumbers
        assert dataset.keywords == keywords
        assert dataset.language == ["English"]
        assert dataset.notesText == notesText
        assert dataset.otherIds == otherIds
        assert dataset.publications == publications
        assert dataset.series == series
        assert dataset.timePeriodsCovered == timePeriodsCovered
        assert dataset.license == "Attribution 4.0 International"
        assert dataset.termsOfUse == "Attribution 4.0 International"


def test_whoas_returns_datasets(dspace_oai_xml_records):
    oai_client = MagicMock()
    oai_client.__next__.return_value = next(iter(dspace_oai_xml_records))
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/oai", text=dspace_oai_xml_records[0],
        )
        whoas = WHOAS(oai_client)
        assert (
            next(whoas).title == "The Title"
        )  # Not sure how deep we want to go with the testing
