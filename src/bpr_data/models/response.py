from dataclasses import dataclass
from src.bpr_data.models.mongo_document_base import SerializableObject


@dataclass
class ApiResponse(SerializableObject):
    response: str
