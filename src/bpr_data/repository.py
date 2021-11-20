from __future__ import annotations

from enum import Enum
import pymongo as mongo
from bson.objectid import ObjectId

from .models.mongo_document_base import MongoDocumentBase, SerializableObject


class Collection(Enum):
    APPLICATION_LOG = 'application_log'
    WORKSPACE = "workspace"
    USER = "user"
    TEAM = 'team'
    INVITATION = 'invitation'
    PROJECT = 'project'
    TESTING = 'testing'
    DIAGRAM = 'diagram'
    MODEL = 'model'
    MODEL_REPRESENTATION = 'model_representation'


class Repository:
    __instance = None
    __client = None

    _protocol = ""
    _user = ""
    _pw = ""
    _host = ""
    _default_db = ""

    @staticmethod
    def get_instance(protocol, user, pw, host, default_db) -> Repository:
        if Repository.__instance is None:
            Repository(protocol, user, pw, host, default_db)
        return Repository.__instance

    def __init__(self, protocol, user, pw, host, default_db):
        if Repository.__instance is not None:
            raise Exception("Singleton class! Use get_instance()")
        else:
            Repository.__instance = self
            Repository._protocol = protocol
            Repository._user = user
            Repository._pw = pw
            Repository._host = host
            Repository._default_db = default_db

    def insert(self, collection: Collection, item: MongoDocumentBase) -> dict:
        """
        Inserts a document into the given collection.
        Note that the _id field will be ignored on insertion
        :param collection: Collection to insert into
        :param item: the item to insert
        :return: the inserted item with its given id
        """
        d = item.as_dict()
        # NOTE: We always delete the _id field, since MongoDB should handle that
        # This also removes issues where errors has led to garbage values in the _id field
        if '_id' in d:
            del d['_id']

        result = self.__get_collection(collection).insert_one(d)
        if result.acknowledged:
            return self.find_one(collection, _id=result.inserted_id)

    def find(self, collection: Collection, **kwargs) -> list:
        """
        Find all items matching the query in kwargs.
        Note that `_id` must be of type ObjectId if used.
        A special parameter, `id`, will automatically be converted from string to ObjectId and be used in the query as `_id`.
        :param collection: collection to search
        :param kwargs: search params in key-value form
        :return: the resulting list of items as dicts
        """
        if kwargs.get('id') is not None:
            if isinstance(kwargs['id'], str):
                kwargs['_id'] = ObjectId(kwargs['id'])
            del kwargs['id']

        if kwargs.get('nested_conditions') is not None:
            nested_conditions = kwargs.get('nested_conditions')
            for item in nested_conditions.keys():
                kwargs[item] = nested_conditions[item]
            kwargs.pop("nested_conditions")

        return list(self.__get_collection(collection).find(kwargs))

    def find_one(self, collection: Collection, **kwargs) -> dict:
        """
        Find the first item that matches the query in kwargs.
        Note that `_id` must be of type ObjectId if used.
        A special parameter, `id`, will automatically be converted from string to ObjectId and be used in the query as `_id`.
        :param collection: collection to search
        :param kwargs: search params in key-value form
        :return: the first item matching the query
        """
        if kwargs.get('id') is not None:
            if isinstance(kwargs['id'], str):
                kwargs['_id'] = ObjectId(kwargs['id'])
            del kwargs['id']

        return self.__get_collection(collection).find_one(kwargs)

    def delete(self, collection: Collection, **kwargs) -> bool:
        """
        Delete the first item that matches the query in kwargs.
        Note that `_id` must be of type ObjectId if used.
        A special parameter, `id`, will automatically be converted from string to ObjectId and be used in the query as `_id`.
        :param collection: collection to delete from
        :param kwargs: search params in key-value form
        :return: True if an item was deleted, otherwise False
        """
        if kwargs.get('id') is not None:
            if isinstance(kwargs['id'], str):
                kwargs['_id'] = ObjectId(kwargs['id'])
            del kwargs['id']
        delete_result = self.__get_collection(collection).delete_one(kwargs)
        return delete_result.deleted_count > 0

    def __purge(self, collection: Collection):
        """
        Utility function that deletes all items in a given collection
        Intended for testing purposes, do not use in code
        :param collection: collection to query
        :return:
        """
        self.__get_collection(collection).delete_many({})

    def update(self, collection: Collection, item: MongoDocumentBase) -> dict:
        """
        Updates a document with new values.
        Document is found by _id
        :param collection: collection to query
        :param item: item to update
        :return: updated item
        """
        query = {'_id': item.id}

        update_values = item.as_dict()
        if '_id' in update_values:
            del update_values['_id']
        values = {'$set': update_values}

        self.__get_collection(collection).update_one(query, values)
        return self.find_one(collection, _id=item.id)

    def push(self, collection: Collection, document_id: ObjectId, field_name: str, item) -> bool:
        """
        Inserts an item into a list on a document.
        :rtype: object
        :param collection: collection to query
        :param document_id:document id
        :param field_name: list field on document
        :param item: Document to modify
        :return:  True if a document was modified
        """
        if isinstance(item, SerializableObject) or isinstance(item, MongoDocumentBase):
            item = item.as_dict()

        # NOTE: Consider changing $push to $addToSet to avoid dupes in list
        update_result = self.__get_collection(collection).update_one(
            {'_id': ObjectId(document_id)},
            {'$addToSet': {field_name: item}}
        )
        return update_result.modified_count > 0

    def push_list(self, collection: Collection, document_id: ObjectId, field_name: str, items: list) -> bool:
        """
        Inserts item into a list on a document.
        :rtype: object
        :param collection: collection to query
        :param document_id:document id
        :param field_name: list field on document
        :param items: Documents to add
        :return:  True if a document was modified
        """
        if len(items) > 0:
            if isinstance(items[0], SerializableObject) or isinstance(items[0], MongoDocumentBase):
                items = SerializableObject.as_dict_list(items)

            # NOTE: Consider changing $push to $addToSet to avoid dupes in list
            update_result = self.__get_collection(collection).update_one(
                {'_id': ObjectId(document_id)},
                {'$addToSet': {field_name: {'$each': items}}}
            )
            return update_result.modified_count > 0

    def pull(self, collection: Collection, document_id: ObjectId, field_name: str, item) -> bool:
        """
        Removes an item from a list on a document.
        :param collection: collection to query
        :param document_id: document id
        :param field_name: list field on document
        :param item: Document to modify
        :return: True if a document was modified
        """
        update_result = self.__get_collection(collection).update_one(
            {'_id': ObjectId(document_id)},
            {'$pull': {field_name: item}}
        )

        return update_result.modified_count > 0

    def join(
            self,
            local_collection: Collection,
            local_field: str,
            foreign_collection: Collection,
            foreign_field: str,
            to_field: str,
            unwind: bool = False,
            **match_args) -> list:
        """
        Returns results from the `local_collection` with the matching documents in the `foreign_collection` as sub-documents.

        Equivalent to a left outer join.

        If `unwind` is True, an unwind step on to_field is added to the pipeline.
        From MongoDB documentation:
        "Deconstructs an array field from the input documents to output a document for each element.
        Each output document is the input document with the value of the array field replaced by the element."

        A filter step will be added to the beginning of the pipeline if filtering arguments are added to `match_args`.

        :param local_collection: collection add sub-documents to
        :param local_field: field to join on in local collection
        :param foreign_collection: collection to join
        :param foreign_field: field to join on in foreign collection
        :param to_field: field containing the results of the join
        :param unwind: if true, unwinds on to_field
        :param match_args: arguments to filter local collection by
        :return: list of resulting documents
        """

        if 'id' in match_args:
            if match_args['id'] is not None:
                match_args['_id'] = ObjectId(match_args['id'])
            del match_args['id']

        pipeline = [
            {
                '$lookup': {
                    'from': foreign_collection.value,
                    'localField': local_field,
                    'foreignField': foreign_field,
                    'as': to_field
                }
            }
        ]

        if match_args:
            pipeline.insert(0, {'$match': match_args})
        if unwind:
            pipeline.append({'$unwind': f'${to_field}'})

        result = self.__get_collection(local_collection).aggregate(pipeline)
        return list(result)

    def aggregate(self, collection: Collection, pipeline: list) -> dict | list:
        """
        Build custom aggregations on a collection.
        Pass aggregation stages as a dict list to the pipeline argument.
        See https://docs.mongodb.com/manual/core/aggregation-pipeline/ for more information on the aggregation pipeline.
        :param collection: collection to aggregate on
        :param pipeline: list of dicts
        :return: result of aggregation
        """
        return self.__get_collection(collection).aggregate(pipeline=pipeline)

    def __get_collection(self, collection: Collection):
        if self.__client is None:
            self.__client = mongo.MongoClient(
                f'{self._protocol}://{self._user}:{self._pw}@{self._host}/{self._default_db}?retryWrites=true&w=majority')
        db = self.__client.get_default_database()
        return db[collection.value]
