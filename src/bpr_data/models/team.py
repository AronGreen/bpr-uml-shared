from dataclasses import dataclass
from bson import ObjectId

from .mongo_document_base import MongoDocumentBase


@dataclass
class Team(MongoDocumentBase):
    teamName: str
    workspaceId: ObjectId
    users: list