import json

from hoard.sources.jpal import create_from_dataverse_json
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
from hoard.sources.whoas import create_from_whoas_dim_xml


def test_minimal_dataset(dataverse_minimal_json_record):
    author = Author(authorName="Finch, Fiona", authorAffiliation="Birds Inc.")
    contact = Contact(
        datasetContactName="Finch, Fiona", datasetContactEmail="finch@mailinator.com"
    )
    description = Description(
        dsDescriptionValue="Darwin's finches (also known"
        " as the Galápagos finches) are a group of about"
        " fifteen species of passerine birds."
    )
    new_record = Dataset(
        authors=[author],
        contacts=[contact],
        description=[description],
        subjects=["Medicine, Health and Life Sciences"],
        title="Darwin's Finches",
    )
    assert new_record.asdict() == dataverse_minimal_json_record


def test_full_dataset(dataverse_full_json_record):
    author = Author(
        authorName="LastAuthor1, FirstAuthor1",
        authorAffiliation="AuthorAffiliation1",
        authorIdentifier="AuthorIdentifier1",
        authorIdentifierScheme="ORCID",
    )
    contact = Contact(
        datasetContactName="LastContact1, FirstContact1",
        datasetContactEmail="ContactEmail1@mailinator.com",
        datasetContactAffiliation="ContactAffiliation1",
    )
    description = Description(
        dsDescriptionValue="DescriptionText 1", dsDescriptionDate="1000-01-01"
    )
    contributors = Contributor(
        contributorName="LastContributor1, FirstContributor1",
        contributorType="Data Collector",
    )
    distributors = Distributor(
        distributorName="LastDistributor1, FirstDistributor1",
        distributorURL="http://DistributorURL1.org",
    )
    keywords = Keyword(keywordValue="KeywordTerm1")
    grantNumbers = GrantNumber(
        grantNumberValue="GrantInformationGrantNumber1",
        grantNumberAgency="GrantInformationGrantAgency1",
    )
    otherIds = OtherId(
        otherIdValue="OtherIDIdentifier1", otherIdAgency="OtherIDAgency1",
    )
    producers = Producer(
        producerName="LastProducer1, FirstProducer1",
        producerURL="http://ProducerURL1.org",
    )
    publications = Publication(
        publicationCitation="RelatedPublicationCitation1",
        publicationIDNumber="RelatedPublicationIDNumber1",
        publicationIDType="ark",
        publicationURL="http://RelatedPublicationURL1.org",
    )
    series = Series(seriesName="SeriesName", seriesInformation="SeriesInformation")
    timePeriodsCovered = TimePeriodCovered(
        timePeriodCoveredStart="1005-01-01", timePeriodCoveredEnd="1005-01-02",
    )
    new_record = Dataset(
        authors=[author],
        alternativeURL="http://AlternativeURL.org",
        contacts=[contact],
        description=[description],
        subjects=[
            "Agricultural Sciences",
            "Business and Management",
            "Engineering",
            "Law",
        ],
        title="Replication Data for: Title",
        keywords=[keywords],
        otherIds=[otherIds],
        publications=[publications],
        notesText="Notes1",
        producers=[producers],
        productionPlace="ProductionPlace",
        contributors=[contributors],
        grantNumbers=[grantNumbers],
        distributors=[distributors],
        distributionDate="1004-01-01",
        language="Language",
        timePeriodsCovered=[timePeriodsCovered],
        kindOfData=["KindOfData1", "KindOfData2"],
        series=series,
        license="CC0",
        termsOfUse="CC0 Waiver",
    )
    assert json.dumps(new_record.asdict(), sort_keys=True) == json.dumps(
        dataverse_full_json_record, sort_keys=True
    )


def test_create_dataset_from_dataverse_json(dataverse_minimal_json_record):
    dataset = create_from_dataverse_json(dataverse_minimal_json_record)
    assert dataset.asdict() == dataverse_minimal_json_record


def test_create_whoas_dim_xml(whoas_oai_server):
    title = (
        "Animals on the Move and Deep‐Sea Vents: Dataset for Spherical Display Systems"
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
            datasetContactEmail="FAKE_EMAIL@FAKE_DOMAIN.EDU",
        )
    ]
    description = [
        Description(
            dsDescriptionValue="This educational package was developed.",
            dsDescriptionDate=None,
        ),
        Description(dsDescriptionValue="Sample abstract", dsDescriptionDate=None,),
    ]
    subjects = [
        "Migration",
        "Larval dispersal",
    ]
    dataset = create_from_whoas_dim_xml(whoas_oai_server[0])
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == description
    assert dataset.subjects == subjects

    dataset = create_from_whoas_dim_xml(whoas_oai_server[1])
    assert dataset.title == title
    assert dataset.authors == []
    assert dataset.contacts == contacts
    assert dataset.description == []
    assert dataset.subjects == []
