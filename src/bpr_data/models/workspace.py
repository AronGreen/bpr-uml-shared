from dataclasses import dataclass, field

from src.bpr_data.models.mongo_document_base import MongoDocumentBase


@dataclass
class Workspace(MongoDocumentBase):
    name: str
    users: list
