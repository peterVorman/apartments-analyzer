import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError, BulkWriteError

from analyzer.exceptions import DuplicatedUniqueField

LOGGER = logging.getLogger(__name__)


class BaseStorage:
    collection_name = ""
    indexes = ()
    id_field = "_id"
    domain_class = None

    def __init__(self, loop, host, port, db_name):
        self.loop = loop
        self.db_name = db_name
        self._client = AsyncIOMotorClient(host=host,
                                          port=port,
                                          document_class=dict)
        self._db = None
        self._collection = None
        self._is_connected = False

    @property
    def is_connected(self):
        return self._is_connected

    async def connect(self):
        if self._is_connected:
            return
        self._db = self._client.get_database(self.db_name)
        existent_collections = await self.get_collection_names()
        if self.collection_name not in existent_collections:
            collection = await self.create_collection()
            LOGGER.debug("Created collection '{}'".format(self.collection_name))
            for index in self.indexes:
                LOGGER.debug("Created index '{}'".format(index.get("name")))
                await collection.create_index(**index)
        self._collection = AsyncIOMotorCollection(self._db, self.collection_name)
        self._is_connected = True

    async def get_dbs(self):
        return await self._client.database_names()

    async def get_collection_names(self):
        return await self._db.collection_names()

    async def create_collection(self):
        return await self._db.create_collection(self.collection_name)

    async def drop_collection(self):
        await self._collection.drop()
        self._is_connected = False

    async def insert(self, obj):
        try:
            LOGGER.info("Insert obj with {}:{}".format(self.id_field, getattr(obj, self.id_field)))
            return await self._collection.insert_one(self.obj_to_dict(obj))
        except DuplicateKeyError as e:
            index_name = e.details['errmsg'].split(":")[2][:-8].strip()
            index_keys = None
            for index in self.indexes:
                if index["name"] == index_name:
                    index_keys = index.get("keys")
                    break
            if index_keys == self.id_field:
                LOGGER.info("Obj with {}:{} already exists.".format(self.id_field, getattr(obj, self.id_field)))
                return await self.update({self.id_field: getattr(obj, self.id_field)}, obj)
            else:
                raise DuplicatedUniqueField(index_keys)

    async def insert_many(self, documents):
        try:
            if documents:
                return await self._collection.insert_many([self.obj_to_dict(obj)for obj in documents])
        except (DuplicateKeyError, BulkWriteError):
            # LOGGER.info("Obj {} already exists.".format(obj.offer_id))
            # await self.update({self.id_field: getattr(obj, self.id_field)}, obj)
            pass

    async def update(self, obj_filter, obj):
        LOGGER.info("Update obj {}:{}".format(self.id_field, getattr(obj, self.id_field)))
        return await self._collection.update_one(obj_filter, {'$set': self.obj_to_dict(obj)})

    async def find_by_id(self, id_value):
        data = await self._collection.find_one({self.id_field: id_value})
        return self.dict_to_obj(data)

    @staticmethod
    def obj_to_dict(obj):
        offer_dict = dict()
        offer_dict.update(obj.__dict__)
        return offer_dict

    def dict_to_obj(self, dict_data):
        del dict_data["_id"]
        return self.domain_class(**dict_data)


class OfferStorage(BaseStorage):
    collection_name = "offers"
    indexes = (
        {
            "keys": "offer_id",
            "name": "by offer id",
            "unique": True,
        },
        {
            "keys": "phones",
            "name": "by phones",
            "unique": False,
        }
    )
    id_field = "offer_id"


class PhoneStorage(BaseStorage):
    collection_name = "phones"
    indexes = (
        {
            "keys": "phone",
            "name": "by by phone",
            "unique": True,
        },
    )
    id_field = "offer_id"