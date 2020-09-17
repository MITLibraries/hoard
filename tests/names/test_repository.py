from hoard.names.db import engine
from hoard.names.repository import Warehouse


def test_warehouse_finds_author(warehouse_data):
    warehouse = Warehouse(engine())

    results = list(warehouse.find(first="Temper", middle="F", last="Joiner"))
    assert results == [("temperance", "Joiner, Temperance F", None)]

    results = list(warehouse.find(first="", middle="", last="Joiner"))
    assert ("temperance", "Joiner, Temperance F", None) in results
    assert ("silence", "Joiner, Silence G", None) in results

    results = list(warehouse.find(first="I", middle="D", last="Briggs"))
    assert ("increase", "Briggs, Increase D", "0000-0000-0001") in results

    results = list(warehouse.find(last="Durance"))
    assert ("honor", "Durance, Honor E", "0000-0000-0000") in results
