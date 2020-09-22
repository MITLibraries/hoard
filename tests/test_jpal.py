import json
import requests_mock
from unittest.mock import MagicMock

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
from hoard.sources.jpal import create_from_dataverse_json, JPAL


def test_jpal_returns_datasets(
    dataset, dataverse_minimal_json_record, dataverse_oai_xml_records
):
    oai_client = MagicMock()
    oai_client.__next__.return_value = next(iter(dataverse_oai_xml_records))
    with requests_mock.Mocker() as m:
        m.get(
            "http+mock://example.com/api/datasets/export?"
            "exporter=dataverse_json&persistentId=12345",
            json=dataverse_minimal_json_record,
        )
        jpal = JPAL(oai_client)
        assert type(next(jpal)) == Dataset


def test_create_dataset_from_minimal_dataverse_json(shared_datadir):
    json_record = json.loads(
        (shared_datadir / "jpal/jpal_minimal_record.json").read_text()
    )
    actual = create_from_dataverse_json(json_record)
    expected = Dataset(
        alternativeURL="https://doi.org/00.0000/DVN/00002",
        authors=[Author(authorName="Finch, Fiona", authorAffiliation="Birds Inc.")],
        contacts=[
            Contact(
                datasetContactName="Finch, Fiona",
                datasetContactEmail="finch@mailinator.com",
            )
        ],
        description=[
            Description(
                dsDescriptionValue="Darwin's finches (also known"
                " as the Galápagos finches) are a group of about"
                " fifteen species of passerine birds.",
            )
        ],
        distributionDate="2020-01-01",
        distributors=[
            Distributor(
                distributorName="The Abdul Latif Jameel Poverty Action Lab Dataverse",
                distributorURL="https://dataverse.harvard.edu/dataverse/jpal",
            ),
        ],
        subjects=["Medicine, Health and Life Sciences"],
        title="Darwin's Finches",
    )

    assert expected == actual


def test_create_dataset_from_full_dataverse_json(shared_datadir):
    json_record = json.loads(
        (shared_datadir / "jpal/jpal_complete_record.json").read_text()
    )
    actual = create_from_dataverse_json(json_record)
    expected = Dataset(
        alternativeURL="https://doi.org/00.0000/DVN/00001",
        authors=[
            Author(
                authorAffiliation="AuthorAffiliation1",
                authorIdentifier="AuthorIdentifier1",
                authorIdentifierScheme="ORCID",
                authorName="LastAuthor1, FirstAuthor1",
            ),
            Author(
                authorAffiliation="AuthorAffiliation2",
                authorIdentifier="AuthorIdentifier2",
                authorIdentifierScheme="ORCID",
                authorName="LastAuthor2, FirstAuthor2",
            ),
        ],
        contacts=[
            Contact(
                datasetContactAffiliation="ContactAffiliation1",
                datasetContactEmail="ContactEmail1@mailinator.com",
                datasetContactName="LastContact1, FirstContact1",
            ),
            Contact(
                datasetContactAffiliation="ContactAffiliation2",
                datasetContactEmail="ContactEmail2@mailinator.com",
                datasetContactName="LastContact2, FirstContact2",
            ),
        ],
        contributors=[
            Contributor(
                contributorName="LastContributor1, FirstContributor1",
                contributorType="Data Collector",
            ),
            Contributor(
                contributorName="LastContributor2, FirstContributor2",
                contributorType="Researcher",
            ),
        ],
        description=[
            Description(
                dsDescriptionDate="2020-01-01", dsDescriptionValue="DescriptionText 1",
            ),
            Description(dsDescriptionValue="DescriptionText 2"),
        ],
        distributionDate="2020-06-27",
        distributors=[
            Distributor(
                distributorName="The Abdul Latif Jameel Poverty Action Lab Dataverse",
                distributorURL="https://dataverse.harvard.edu/dataverse/jpal",
            ),
            Distributor(
                distributorName="LastDistributor1, FirstDistributor1",
                distributorURL="http://DistributorURL1.org",
            ),
            Distributor(
                distributorName="LastDistributor2, FirstDistributor2",
                distributorURL="http://DistributorURL2.org",
            ),
        ],
        grantNumbers=[
            GrantNumber(
                grantNumberAgency="GrantInformationGrantAgency1",
                grantNumberValue="GrantInformationGrantNumber1",
            )
        ],
        keywords=[
            Keyword(keywordValue="KeywordTerm1"),
            Keyword(keywordValue="KeywordTerm2"),
        ],
        kindOfData=["KindOfData1", "KindOfData2"],
        language=["English", "Swahili"],
        license="CC0",
        notesText="Notes1",
        otherIds=[
            OtherId(otherIdAgency="OtherIDAgency1", otherIdValue="OtherIDIdentifier1",),
            OtherId(otherIdAgency="OtherIDAgency2", otherIdValue="OtherIDIdentifier2",),
        ],
        producers=[
            Producer(
                producerName="LastProducer1, FirstProducer1",
                producerURL="http://ProducerURL1.org",
            ),
            Producer(
                producerName="LastProducer2, FirstProducer2",
                producerURL="http://ProducerURL2.org",
            ),
        ],
        productionPlace="ProductionPlace",
        publications=[
            Publication(
                publicationCitation="RelatedPublicationCitation1",
                publicationIDNumber="RelatedPublicationIDNumber1",
                publicationIDType="ark",
                publicationURL="http://RelatedPublicationURL1.org",
            ),
            Publication(
                publicationCitation="RelatedPublicationCitation2",
                publicationIDNumber="RelatedPublicationIDNumber2",
                publicationIDType="doi",
                publicationURL="https://doi.org/RelatedPublicationURL2",
            ),
        ],
        series=Series(seriesInformation="SeriesInformation", seriesName="SeriesName",),
        subjects=[
            "Agricultural Sciences",
            "Business and Management",
            "Engineering",
            "Law",
        ],
        termsOfUse="CC0 Waiver",
        timePeriodsCovered=[
            TimePeriodCovered(
                timePeriodCoveredStart="1005-01-01", timePeriodCoveredEnd="1005-01-02",
            ),
            TimePeriodCovered(
                timePeriodCoveredStart="2020-01-01", timePeriodCoveredEnd="2020-01-02",
            ),
        ],
        title="Replication Data for: Title",
    )

    assert expected == actual
