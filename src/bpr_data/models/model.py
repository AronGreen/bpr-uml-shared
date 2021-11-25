from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TypeVar, List

from bson import ObjectId

from .mongo_document_base import MongoDocumentBase, SerializableObject


@dataclass
class Model(MongoDocumentBase):
    type: str
    projectId: ObjectId
    path: str
    history: list  # type: HistoryBaseAction
    relations: list  # type: Relation
    attributes: list  # type: AttributeBase


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

    @staticmethod
    def parse(data: str | dict):
        """
        Converts the given data to the correct type inferred by the `type` field in the data.
        :param data: json or dict with a representation of a subclass of AttributeBase
        :return: the parsed AttributeBase subclass
        """
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise TypeError
        if 'kind' not in data:
            raise KeyError

        # Add additional types here
        if data['kind'] == 'field':
            return Field.from_dict(data)
        if data['kind'] == 'method':
            return Method.from_dict(data)
        else:
            return Property.from_dict(data)


@dataclass
class Property(AttributeBase):
    """Catch all attribute type"""
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
    kind: str = "field"


@dataclass
class Method(MemberBaseModel):
    parameters: list  # type: MethodParameter
    kind: str = "method"


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
    itemId: ObjectId
    action = "removeAttribute"


@dataclass
class SetAttributeAction(HistoryBaseAction):
    oldItem: AttributeBase
    newItem: AttributeBase
    action = "setAttribute"


AttributeType = TypeVar('AttributeType', bound=AttributeBase)
HistoryActionType = TypeVar('HistoryActionType', bound=HistoryBaseAction)
