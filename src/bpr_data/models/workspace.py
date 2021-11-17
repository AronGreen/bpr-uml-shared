from dataclasses import dataclass, field

from ..models.mongo_document_base import MongoDocumentBase


@dataclass
class Workspace(MongoDocumentBase):
    name: str
    users: list
