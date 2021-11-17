from dataclasses import dataclass

from bson import ObjectId
from src.bpr_data.models.mongo_document_base import MongoDocumentBase


@dataclass
class Diagram(MongoDocumentBase):
    title: str
    projectId: ObjectId
    path: str
    models: list  # representations
