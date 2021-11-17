from dataclasses import dataclass
from ..models.mongo_document_base import SerializableObject


@dataclass
class ApiResponse(SerializableObject):
    response: str
