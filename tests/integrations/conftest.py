import asyncio

from pytest import fixture

from analyzer.storages import BaseStorage

LOOP = asyncio.get_event_loop()


class SimpleObj:
    def __init__(self, key, unique, not_unique):
        self.key = key
        self.unique = unique
        self.not_unique = not_unique

    def __eq__(self, other):
        return self.key == other.key and self.unique == other.unique and self.not_unique == other.not_unique


class Storage(BaseStorage):
    collection_name = "testcollection"
    indexes = (
        {
            "keys": "key",
            "name": "by key",
            "unique": True,
        },
        {
            "keys": "unique",
            "name": "by unique",
            "unique": True,
        },
        {
            "keys": "not_unique",
            "name": "by not_unique",
            "unique": False,
        },
    )
    id_field = "key"
    domain_class = SimpleObj


@fixture
def test_storage(config, event_loop):
    storage = Storage(db_name=config["db_name"],
                      host=config["host"],
                      port=config["port"],
                      loop=event_loop)
    event_loop.run_until_complete(storage.connect())
    yield storage
    event_loop.run_until_complete(storage.drop_collection())
