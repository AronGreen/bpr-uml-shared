from dataclasses import dataclass
from bson.objectid import ObjectId
from .mongo_document_base import MongoDocumentBase, ObjectIdReferencer


@dataclass
class Project(MongoDocumentBase):
    title: str
    workspaceId: ObjectId
    users: list  # ProjectUser
    teams: list  # ProjectTeam


@dataclass
class ProjectUser(ObjectIdReferencer):
    userId: ObjectId
    isEditor: bool


@dataclass
class ProjectTeam(ObjectIdReferencer):
    teamId: ObjectId
    isEditor: bool
