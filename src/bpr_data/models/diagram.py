from dataclasses import dataclass

from bson import ObjectId
from mongo_document_base import MongoDocumentBase


@dataclass
class Diagram(MongoDocumentBase):
    title: str
    projectId: ObjectId
    path: str
    models: list  # representations
