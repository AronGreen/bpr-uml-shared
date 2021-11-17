from dataclasses import dataclass
from bson.objectid import ObjectId
from src.bpr_data.models.mongo_document_base import MongoDocumentBase, SerializableObject


@dataclass
class Project(MongoDocumentBase):
    title: str
    workspaceId: ObjectId
    users: list  # ProjectUser
    teams: list  # ProjectTeam


@dataclass
class ObjectIdReferencer(SerializableObject):

    @classmethod
    def to_object_ids(cls, field_name: str, objects: list):
        for obj in objects:
            setattr(obj, field_name, ObjectId(getattr(obj, field_name)))
        return objects


@dataclass
class ProjectUser(ObjectIdReferencer):
    userId: ObjectId
    isEditor: bool


@dataclass
class ProjectTeam(ObjectIdReferencer):
    teamId: ObjectId
    isEditor: bool
