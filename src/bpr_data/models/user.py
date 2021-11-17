from dataclasses import dataclass
from mongo_document_base import MongoDocumentBase


@dataclass
class User(MongoDocumentBase):
    name: str
    email: str
    firebaseId: str
