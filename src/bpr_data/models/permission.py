from enum import Enum, auto


class WorkspacePermission(str, Enum):
    MANAGE_TEAMS = "MANAGE_TEAMS"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"
    MANAGE_WORKSPACE = "MANAGE_WORKSPACE"