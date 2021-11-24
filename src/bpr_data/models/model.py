from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar, List

from bson import ObjectId

from .mongo_document_base import MongoDocumentBase, SerializableObject


@dataclass
class Model(MongoDocumentBase):
    type: str
    projectId: ObjectId
    path: str
    history: List[HistoryBaseAction]
    relations: List[Relation]
    attributes: List[AttributeBase]


@dataclass
class ModelRepresentation(MongoDocumentBase):
    modelId: ObjectId
    diagramId: ObjectId
    x: float
    y: float
    w: float
    h: float


@dataclass
class FullModelRepresentation(ModelRepresentation):
    model: Model


@dataclass
class Relation(MongoDocumentBase):
    target: ObjectId
    type: str
    accessModifier: str
    parentCardinality: str
    childCardinality: str
    parentName: str
    childName: str
    name: str


@dataclass
class RelationRepresentation(SerializableObject):
    relationId: ObjectId
    # TODO: define data needed.


# ATTRIBUTE TYPES

@dataclass
class AttributeBase(MongoDocumentBase):
    """
    Abstract
    """
    kind = None


@dataclass
class Property(AttributeBase):
    value: ...
    kind: str


@dataclass
class MemberBaseModel(AttributeBase):
    """
    Abstract
    """
    name: str
    type: str
    accessModifier: str


@dataclass
class Field(MemberBaseModel):
    kind = "field"


@dataclass
class Method(MemberBaseModel):
    parameters: List[MethodParameter]
    kind = "method"


@dataclass
class MethodParameter(SerializableObject):
    name: str
    type: str


# MODEL ACTIONS
# remember to add action field!

@dataclass
class HistoryBaseAction(SerializableObject):
    timestamp: str
    userId: ObjectId
    action = None


@dataclass
class CreateModelAction(HistoryBaseAction):
    action = "createModel"


@dataclass
class AddAttributeAction(HistoryBaseAction):
    item: AttributeBase
    action = "addAttribute"


@dataclass
class RemoveAttributeAction(HistoryBaseAction):
    item: AttributeBase
    itemId: ObjectId
    action = "removeAttribute"


@dataclass
class SetAttributeAction(HistoryBaseAction):
    oldItem: AttributeBase
    newItem: AttributeBase
    action = "setAttribute"


AttributeType = TypeVar('AttributeType', bound=AttributeBase)
HistoryActionType = TypeVar('HistoryActionType', bound=HistoryBaseAction)
