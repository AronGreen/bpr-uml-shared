from enum import Enum
from dataclasses import dataclass

@dataclass
class WorkspacePermission(str, Enum):
    MANAGE_TEAMS = "MANAGE_TEAMS"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"
    MANAGE_WORKSPACE = "MANAGE_WORKSPACE"

    @classmethod
    def convert_strings_to_workspace_permissions_enums(cls, permissions: list):
        enum_permissions = []
        for permission in permissions:
            enum_permissions.append(WorkspacePermission(permission))
        return enum_permissions