from dataclasses import dataclass
from typing import Optional
from .mongo_document_base import MongoDocumentBase


@dataclass
class SomeItem(MongoDocumentBase):
    """
    Dummy class for testing.
    Represents nothing in the domain.
    """
    number: int
    text: str
    users: list
    random: Optional[str] = None


