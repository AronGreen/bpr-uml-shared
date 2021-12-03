from enum import Enum, auto


class Permission(Enum):
    MANAGE_PROJECTS = auto()
    MANAGE_TEAMS = auto()
    MANAGE_PERMISSIONS = auto()
    MANAGE_WORKSPACE = auto()
    MANAGE_USERS = auto()