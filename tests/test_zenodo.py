from unittest.mock import MagicMock

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


from hoard.sources.zenodo import create_from_zenodo_datacite_xml, Zenodo


def test_create_from_zenodo_datacite_xml(zenodo_oai_server):
    client = OAIClient("http+mock://example.com/oai", "dim", "Test_Collection")
    title = "CMIP5 P50 Analysis v1.0 for Tuna Species: Source Data"
    authors = [
        Author(
            authorName="Mislan, K. A. S.",
            authorAffiliation="University of Washington",
            authorIdentifierScheme=None,
            authorIdentifier=None,
        ),
        Author(
            authorName="Brill, Richard W.",
            authorAffiliation="NOAA Northeast Fisheries Science Center",
            authorIdentifierScheme=None,
            authorIdentifier=None,
        ),
    ]
    contacts = [Contact(datasetContactName="!!!!!!", datasetContactEmail="!!!!!!")]
    description = [
        Description(
            dsDescriptionValue="Model results and data used to make future",
            dsDescriptionDate=None,
        ),
        Description(dsDescriptionValue="Sample abstract", dsDescriptionDate=None),
    ]
    keywords = [
        Keyword(keywordValue="tuna"),
        Keyword(keywordValue="climate change"),
    ]
    contributors = [
        Contributor(contributorName="Movahedian,Vafa", contributorType=None)
    ]
    producers = [Producer(producerName="Zenodo", producerURL=None)]
    otherIds = [
        OtherId(otherIdValue="https://zenodo.org/record/807749", otherIdAgency=None),
    ]
    otherIds_2 = [
        OtherId(otherIdValue="https://zenodo.org/record/807752", otherIdAgency=None)
    ]
    otherIds_3 = [
        OtherId(otherIdValue="https://zenodo.org/record/807753", otherIdAgency=None)
    ]
    publications = [
        Publication(
            publicationIDNumber="https://github.com/kallisons/CMIP5_p50_tuna/tree/v1.0",
            publicationIDType="URL",
        )
    ]
    rights = (
        "Creative Commons Attribution Non Commercial 4.0 International. Open Access"
    )

    # minimal record
    subjects = ["!!!!!!"]
    dataset = create_from_zenodo_datacite_xml(zenodo_oai_server[0], client)
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == description
    assert dataset.subjects == subjects

    # full record
    dataset = create_from_zenodo_datacite_xml(zenodo_oai_server[1], client)
    for _k, v in dataset.__dict__.items():
        assert v != []
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == description
    assert dataset.subjects == subjects
    assert dataset.distributionDate == "2017-06-13"
    assert dataset.alternativeURL == "10.5281/zenodo.807748"
    assert dataset.otherIds == otherIds
    assert dataset.keywords == keywords
    assert dataset.kindOfData == ["Dataset"]
    assert dataset.contributors == contributors
    assert dataset.producers == producers
    assert dataset.publications == publications
    assert dataset.language == ["English"]
    assert dataset.license == rights
    assert dataset.termsOfUse == rights

    # record with no description
    dataset = create_from_zenodo_datacite_xml(zenodo_oai_server[4], client)
    for _k, v in dataset.__dict__.items():
        assert v != []
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == [Description(dsDescriptionValue=title)]
    assert dataset.subjects == subjects
    assert dataset.distributionDate == "2017-06-13"
    assert dataset.alternativeURL == "10.5281/zenodo.807752"
    assert dataset.otherIds == otherIds_2
    assert dataset.keywords == keywords
    assert dataset.kindOfData == ["Dataset"]
    assert dataset.contributors == contributors
    assert dataset.producers == producers
    assert dataset.publications == publications
    assert dataset.language == ["English"]
    assert dataset.license == rights
    assert dataset.termsOfUse == rights

    # record with invalid date
    dataset = create_from_zenodo_datacite_xml(zenodo_oai_server[5], client)
    for _k, v in dataset.__dict__.items():
        assert v != []
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == description
    assert dataset.subjects == subjects
    assert dataset.distributionDate is None
    assert dataset.alternativeURL == "10.5281/zenodo.807753"
    assert dataset.otherIds == otherIds_3
    assert dataset.keywords == keywords
    assert dataset.kindOfData == ["Dataset"]
    assert dataset.contributors == contributors
    assert dataset.producers == producers
    assert dataset.publications == publications
    assert dataset.language == ["English"]
    assert dataset.license == rights
    assert dataset.termsOfUse == rights


def test_zendodo_returns_datasets(zenodo_oai_server):
    oai_client = MagicMock()
    oai_client.__next__.return_value = next(iter(zenodo_oai_server))
    records = Zenodo(oai_client)
    assert type(next(records)) == Dataset
    assert next(records).title is not None
    assert next(records).authors is not None
    assert next(records).description is not None
