from __future__ import annotations

import json
from dataclasses import dataclass

from bson import ObjectId

from .mongo_document_base import MongoDocumentBase, SerializableObject


@dataclass
class Model(MongoDocumentBase):
    """
    Base class for all model types.
    Classes inheriting from this class must specify the field `type` with the class name in camelCase.
    In addition to the conversion methods inherited from MongoDocumentBase, a parse method is added
    that can convert json or dict into the concrete model
    """
    type = None
    projectId: ObjectId
    path: str
    history: list

    @staticmethod
    def parse(data: str | dict):
        """
        Converts the given data to the correct type inferred by the `type` field in the data.
        :param data: json or dict with a representation of a subclass of Model
        :return: the parsed Model subclass
        """
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise TypeError
        if 'type' not in data:
            raise KeyError

        # Add additional types here
        if data['type'] == TextBoxModel.type:
            return TextBoxModel.from_dict(data)
        if data['type'] == ClassModel.type:
            return ClassModel.from_dict(data)


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


# MODEL ACTIONS
# remember to add action field!

@dataclass
class ModelHistoryBaseAction(SerializableObject):
    timestamp: str
    userId: ObjectId
    action = None


@dataclass
class CreateAction(ModelHistoryBaseAction):
    action: str = "create"


@dataclass
class AddFieldAction(ModelHistoryBaseAction):
    filed: ModelField
    action: str = "addField"


@dataclass
class RemoveFieldAction(ModelHistoryBaseAction):
    fieldId: ObjectId
    action: str = "removeField"


@dataclass
class AddMethodAction(ModelHistoryBaseAction):
    filed: ModelField
    action: str = "addMethod"


@dataclass
class RemoveMethodAction(ModelHistoryBaseAction):
    fieldId: ObjectId
    action: str = "removeMethod"


@dataclass
class SetNameAction(ModelHistoryBaseAction):
    name: str
    action: str = "setName"


# CONCRETE MODEL CLASSES
# remember to add type field!

@dataclass
class ClassModel(Model):
    name: str
    fields: list  # type: ModelField
    methods: list  # type: ModelMethod
    type: str = 'class'


@dataclass
class TextBoxModel(Model):
    text: str
    type: str = 'textBox'


# MODEL PROPERTY TYPES

@dataclass
class ModelField(MongoDocumentBase):
    name: str
    type: str
    accessModifier: str


@dataclass
class ModelMethod(MongoDocumentBase):
    name: str
    type: str
    accessModifier: str
