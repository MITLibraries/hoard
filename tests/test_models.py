from hoard.models import (
    Author,
    Contact,
    create_from_dataverse_json,
    create_from_dublin_core_xml,
    Dataset,
    Description,
)


def test_dataset(dataverse_json_record):
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
    assert new_record.asdict() == dataverse_json_record


def test_create_dataset_from_dataverse_json(dataverse_json_record):
    dataset = create_from_dataverse_json(dataverse_json_record)
    assert dataset.asdict() == dataverse_json_record


def test_create_dublin_core_xml(whoas_oai_server):
    title = (
        "Mesoplodon densirostris El Hierro, Canary "
        "Islands, Spain 10/11/2003 Animal a Depth Profile"
    )
    authors = [
        Author(
            authorName="Johnson, Mark P.",
            authorAffiliation="",
            authorIdentifierScheme=None,
            authorIdentifierValue=None,
        ),
        Author(
            authorName="Aguilar De Soto, Natacha",
            authorAffiliation="",
            authorIdentifierScheme=None,
            authorIdentifierValue=None,
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
            dsDescriptionValue="Original Sampling Rate: 50 Hz, "
            "Sampling Rate of this file: 1Hz, Channels: 1, Resolution: "
            ".05 meters, Recording device: DTAG serial number 207, Filter: 4Hz",
            dsDescriptionDate=None,
        ),
        Description(
            dsDescriptionValue="DTAG data from a tagged Blainville's beaked "
            "whale; depth (m) over time (s). Location: El Hierro, Canary Islands, "
            "Spain, Species: Mesoplodon densirostris (Blainville's Beaked Whale), "
            "Permit: Granted to ULL from the Canary Island Government (no permit "
            "number), Water Depth: 65m",
            dsDescriptionDate=None,
        ),
    ]
    subjects = [
        "Depth Profile - Blainville's Beaked Whale",
        "Depth Profile - Orca Whale",
    ]
    dataset = create_from_dublin_core_xml(whoas_oai_server[0])
    assert dataset.title == title
    assert dataset.authors == authors
    assert dataset.contacts == contacts
    assert dataset.description == description
    assert dataset.subjects == subjects

    dataset = create_from_dublin_core_xml(whoas_oai_server[1])
    assert dataset.title == title
    assert dataset.authors == []
    assert dataset.contacts == contacts
    assert dataset.description == []
    assert dataset.subjects == []
