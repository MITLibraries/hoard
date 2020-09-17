from unittest.mock import Mock

from hoard.names.service import AuthorService, parse


def test_parse_splits_words():
    assert parse("Foo Bar Baz Gaz") == ("Gaz", "Foo", "Bar")
    assert parse("Foo Bar Baz") == ("Baz", "Foo", "Bar")
    assert parse("Foo Bar") == ("Bar", "Foo", "")


def test_author_service_produces_list_of_names():
    repo = Mock()
    repo.find.return_value = ("one", "two", "three")
    svc = AuthorService(repo)
    assert list(svc.find("foobar")) == [
        ("foobar", "one"),
        ("foobar", "two"),
        ("foobar", "three"),
    ]
