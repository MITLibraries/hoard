import datetime

from hoard.names.db import engine
from hoard.names.repository import Warehouse


def test_warehouse_finds_author(warehouse_data):
    warehouse = Warehouse(engine())

    results = list(warehouse.find(first="Temper", middle="F", last="Joiner"))
    assert results == [
        {
            "kerb": "temperance",
            "name": "Joiner, Temperance F",
            "orcid": None,
            "dlc": "Physics",
            "start_date": datetime.date(2001, 1, 1),
            "end_date": datetime.date(2020, 1, 1),
        }
    ]

    results = list(warehouse.find(first="", middle="", last="Joiner"))
    assert {
        "kerb": "temperance",
        "name": "Joiner, Temperance F",
        "orcid": None,
        "dlc": "Physics",
        "start_date": datetime.date(2001, 1, 1),
        "end_date": datetime.date(2020, 1, 1),
    } in results
    assert {
        "kerb": "silence",
        "name": "Joiner, Silence G",
        "orcid": None,
        "dlc": "Math",
        "start_date": datetime.date(2001, 1, 1),
        "end_date": datetime.date(2020, 1, 1),
    } in results

    results = list(warehouse.find(first="I", middle="D", last="Briggs"))
    assert {
        "kerb": "increase",
        "name": "Briggs, Increase D",
        "orcid": "0000-0000-0001",
        "dlc": "Architecture",
        "start_date": datetime.date(2001, 1, 1),
        "end_date": datetime.date(2020, 1, 1),
    } in results

    results = list(warehouse.find(last="Durance"))
    assert {
        "kerb": "honor",
        "name": "Durance, Honor E",
        "orcid": "0000-0000-0000",
        "dlc": "Philosophy",
        "start_date": datetime.date(2001, 1, 1),
        "end_date": datetime.date(2020, 1, 1),
    } in results
