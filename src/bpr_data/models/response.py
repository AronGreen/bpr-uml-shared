from dataclasses import dataclass
from mongo_document_base import SerializableObject


@dataclass
class ApiResponse(SerializableObject):
    response: str
