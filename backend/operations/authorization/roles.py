from enum import Enum
from typing import List, Dict

class Role(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DEALER = "DEALER"
    BUSINESS_USER = "BUSINESS_USER"
    NORMAL_USER = "NORMAL_USER"
    READ_ONLY = "READ_ONLY"
    SUPPORT_ENGINEER = "SUPPORT_ENGINEER"

class Permission(str, Enum):
    # User Management
    VIEW_USERS = "VIEW_USERS"
    CREATE_USERS = "CREATE_USERS"
    MANAGE_ROLES = "MANAGE_ROLES"
    SUSPEND_USERS = "SUSPEND_USERS"
    
    # System
    VIEW_DASHBOARD = "VIEW_DASHBOARD"
    MANAGE_WORKERS = "MANAGE_WORKERS"
    MANAGE_SCRAPERS = "MANAGE_SCRAPERS"
    MANAGE_SETTINGS = "MANAGE_SETTINGS"
    VIEW_AUDIT_LOGS = "VIEW_AUDIT_LOGS"
    
    # Marketplace
    MANAGE_LISTINGS = "MANAGE_LISTINGS"
    
    # Generic
    BASIC_ACCESS = "BASIC_ACCESS"

ROLE_PERMISSIONS: Dict[Role, List[Permission]] = {
    Role.SUPER_ADMIN: list(Permission),
    Role.ADMIN: [
        Permission.VIEW_USERS, Permission.CREATE_USERS, Permission.SUSPEND_USERS,
        Permission.VIEW_DASHBOARD, Permission.MANAGE_WORKERS, Permission.MANAGE_SCRAPERS,
        Permission.VIEW_AUDIT_LOGS, Permission.BASIC_ACCESS
    ],
    Role.SUPPORT_ENGINEER: [
        Permission.VIEW_USERS, Permission.VIEW_DASHBOARD, Permission.VIEW_AUDIT_LOGS,
        Permission.BASIC_ACCESS
    ],
    Role.DEALER: [
        Permission.MANAGE_LISTINGS, Permission.BASIC_ACCESS
    ],
    Role.BUSINESS_USER: [
        Permission.BASIC_ACCESS
    ],
    Role.NORMAL_USER: [
        Permission.BASIC_ACCESS
    ],
    Role.READ_ONLY: [
        Permission.BASIC_ACCESS
    ]
}

def has_permission(role: str, permission: Permission) -> bool:
    try:
        role_enum = Role(role)
        return permission in ROLE_PERMISSIONS.get(role_enum, [])
    except ValueError:
        return False
