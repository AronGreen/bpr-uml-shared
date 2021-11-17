from dataclasses import dataclass
from bson.objectid import ObjectId
from ..models.mongo_document_base import MongoDocumentBase


@dataclass
class Invitation(MongoDocumentBase):
    inviterId: ObjectId
    workspaceId: ObjectId
    inviteeEmailAddress: str


@dataclass
class InvitationGetModel(Invitation):
    inviterUserName: str
    workspaceName: str
