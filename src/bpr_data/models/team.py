from dataclasses import dataclass
from bson import ObjectId

from .mongo_document_base import MongoDocumentBase, ObjectIdReferencer


@dataclass
class Team(MongoDocumentBase):
    name: str
    workspaceId: ObjectId
    users: list


@dataclass
class TeamUser(ObjectIdReferencer):
    userId: ObjectId
