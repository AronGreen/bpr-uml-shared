from dataclasses import dataclass
from bson import ObjectId

from ..models.mongo_document_base import MongoDocumentBase


@dataclass
class Team(MongoDocumentBase):
    teamName: str
    workspaceId: ObjectId
    users: list