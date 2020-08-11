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


def test_create_dublin_core_xml(dspace_oai_xml_records):
    dataset = create_from_dublin_core_xml(dspace_oai_xml_records[0])
    assert (
        dataset.title == "The Title"
    )  # Not sure how deep we want to go with the testing
    assert dataset.subjects == ["Subject 1"]
