from dataclasses import dataclass, asdict, fields
from bson.objectid import ObjectId
import json


# noinspection PyArgumentList
@dataclass
class SerializableObject:
    """
    Represents a base mongo document.
    Provides conversion methods to and from dict and json.
    Ensures proper conversion between ObjectId and str as needed.
    """

    def as_dict(self):
        """
        Convert to dict
        :return: dict
        """
        return asdict(self)

    def as_json(self):
        """
        Convert to json
        :return: json string
        """
        return json.dumps(asdict(self), default=str)

    @classmethod
    def from_dict(cls, d: dict, set_missing_to_none: bool = False):
        """
        Converts a dictionary to an instance of the calling class.

        Ignores dict fields that are not defined as fields on the calling class.

        Will fail if all required fields are not present in the dict unless set_missing_to_none is set to True
        in which case missing fields will be initialized to None

        :param d: dictionary to convert
        :param set_missing_to_none: If True, sets missing fields in dict to None
        :return: instance of the calling class
        """
        dict_copy = {}
        for key in d:
            if cls.has_field(key):
                dict_copy[key] = d[key]
        if set_missing_to_none:
            for key in [x.name for x in fields(cls)]:
                if key not in dict_copy:
                    dict_copy[key] = None
        return cls(**dict_copy)

    @classmethod
    def as_dict_list(cls, lst: list):
        """
        Convert a list of class instances to a list of dicts
        """
        return [ob.as_dict() for ob in lst]

    @classmethod
    def as_json_list(cls, lst: list):
        """
        Convert a list of class instances to a json list
        """
        return json.dumps(cls.as_dict_list(lst), default=str)

    @classmethod
    def from_json_list(cls, json_list):
        """
        Converts a json list to a list of class instances
        """
        return cls.from_dict_list(json.loads(json_list))

    @classmethod
    def from_dict_list(cls, lst: list):
        """
        Converts a list of dicts to a list of class instances
        """
        return [cls.from_dict(x) for x in lst]

    @classmethod
    def from_json(cls, j: str):
        """
        Converts a json object to an instance of the calling class.

        Ignores fields that are not defined as fields on the calling class.

        Will fail if all required fields are not present in the dict

        Future: Consider adding an option to set missing fields to None

        :param d: json object to convert
        :return: instance of the calling class
        :param j:
        :return:
        """
        return cls.from_dict(json.loads(j))

    @classmethod
    def has_field(cls, field_name: str):
        return field_name in [x.name for x in fields(cls)]

    def get_fields(self):
        return fields(self)

    def __post_init__(self):
        for field in fields(self):
            if isinstance(field.type, ObjectId):
                attr = getattr(self, field.name)
                if attr is not None and isinstance(attr, str):
                    setattr(self, field.name, ObjectId(attr))


@dataclass
class ObjectIdReferencer(SerializableObject):
    @classmethod
    def to_object_ids(cls, field_name: str, objects: list):
        for obj in objects:
            setattr(obj, field_name, ObjectId(getattr(obj, field_name)))
        return objects


@dataclass
class MongoDocumentBase(SerializableObject):
    """
    Represents a base mongo document with an _id property.
    Provides conversion methods to and from dict and json.
    Ensures proper conversion between ObjectId and str as needed.
    """
    _id: ObjectId()

    @property
    def id(self):
        return self._id
