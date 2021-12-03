from enum import Enum, auto


class WorkspacePermission(Enum):
    MANAGE_TEAMS = "MANAGE_TEAMS"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"
    MANAGE_WORKSPACE = "MANAGE_WORKSPACE"
    MANAGE_USERS = "MANAGE_USERS"

class ProjectPermission(Enum):
    MANAGE_PROJECTS = "MANAGE_PROJECTS"