from dataclasses import dataclass, field

from mongo_document_base import MongoDocumentBase


@dataclass
class Workspace(MongoDocumentBase):
    name: str
    users: list
