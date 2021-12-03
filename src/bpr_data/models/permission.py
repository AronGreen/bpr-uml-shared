from enum import Enum, auto

from bpr_data.models.mongo_document_base import SerializableObject


class WorkspacePermission(Enum, SerializableObject):
    MANAGE_TEAMS = "MANAGE_TEAMS"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"
    MANAGE_WORKSPACE = "MANAGE_WORKSPACE"
    MANAGE_USERS = "MANAGE_USERS"

class ProjectPermission(Enum, SerializableObject):
    MANAGE_PROJECTS = "MANAGE_PROJECTS"