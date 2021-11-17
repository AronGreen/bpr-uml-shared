from dataclasses import dataclass
from ..models.mongo_document_base import MongoDocumentBase


@dataclass
class LogItem(MongoDocumentBase):
    timestamp: str
    utcTimestamp: str
    logLevel: str
    note: str
    content: str
