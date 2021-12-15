from dataclasses import dataclass, field

from bson.objectid import ObjectId

from .mongo_document_base import MongoDocumentBase, SerializableObject


@dataclass
class Workspace(MongoDocumentBase):
    name: str
    users: list


@dataclass
class WorkspaceUser(SerializableObject):
    userId: ObjectId
    permissions: list
