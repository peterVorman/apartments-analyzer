import pytest

from analyzer.exceptions import DuplicatedUniqueField
from tests.integrations.conftest import Storage, SimpleObj


@pytest.mark.asyncio
async def test_connect(config, event_loop):
    storage = Storage(db_name=config["db_name"],
                      host=config["host"],
                      port=config["port"],
                      loop=event_loop)
    await storage.connect()
    assert storage.is_connected
    await storage.drop_collection()


@pytest.mark.asyncio
async def test_drop_connection(config, event_loop):
    storage = Storage(db_name=config["db_name"],
                      host=config["host"],
                      port=config["port"],
                      loop=event_loop)
    await storage.connect()
    assert storage.is_connected
    await storage.drop_collection()
    assert not storage.is_connected


@pytest.mark.asyncio
async def test_connect_twice(config, event_loop):
    storage = Storage(db_name=config["db_name"],
                      host=config["host"],
                      port=config["port"],
                      loop=event_loop)
    await storage.connect()
    await storage.connect()
    assert storage.is_connected


@pytest.mark.asyncio
async def test_insert_one(test_storage):
    test_obj = SimpleObj(key=1,
                         unique="unique",
                         not_unique="not_unique")
    await test_storage.insert(test_obj)
    received_obj = await test_storage.find_by_id(test_obj.key)
    assert test_obj == received_obj


@pytest.mark.asyncio
async def test_insert_two_different_objects(test_storage):
    test_obj1 = SimpleObj(key=1,
                          unique="unique",
                          not_unique="not_unique")
    test_obj2 = SimpleObj(key=2,
                          unique="unique1",
                          not_unique="not_unique")

    await test_storage.insert(test_obj1)
    await test_storage.insert(test_obj2)
    received_obj1 = await test_storage.find_by_id(test_obj1.key)
    received_obj2 = await test_storage.find_by_id(test_obj2.key)

    assert test_obj1 == received_obj1
    assert test_obj2 == received_obj2


@pytest.mark.asyncio
async def test_insert_two_objects_with_the_same_unique_field(test_storage):
    test_obj1 = SimpleObj(key=1,
                          unique="unique",
                          not_unique="not_unique")
    test_obj2 = SimpleObj(key=2,
                          unique="unique",
                          not_unique="not_unique")

    await test_storage.insert(test_obj1)

    with pytest.raises(DuplicatedUniqueField):
        await test_storage.insert(test_obj2)


@pytest.mark.asyncio
async def test_insert_two_objects_with_the_same_id_field(test_storage):
    test_obj = SimpleObj(key=1,
                         unique="unique",
                         not_unique="not_unique")
    test_obj_updated = SimpleObj(key=1,
                                 unique="unique1",
                                 not_unique="not_unique1")

    await test_storage.insert(test_obj)
    await test_storage.insert(test_obj_updated)

    received_obj = await test_storage.find_by_id(test_obj.key)

    assert test_obj_updated == received_obj
    assert test_obj != received_obj
