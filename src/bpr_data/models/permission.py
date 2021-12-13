from enum import Enum, auto

from bpr_data.models.mongo_document_base import SerializableObject


class WorkspacePermission(str, Enum):
    MANAGE_TEAMS = "MANAGE_TEAMS"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"
    MANAGE_WORKSPACE = "MANAGE_WORKSPACE"

    def convert_strings_to_workspace_permissions_enums(permissions: list):
        enum_permissions = []
        for permission in permissions:
            enum_permissions.append(WorkspacePermission(permission))
        return enum_permissions