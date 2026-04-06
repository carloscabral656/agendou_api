from enum import StrEnum


class UserRole(StrEnum):
    super_admin = "super_admin"
    company_admin = "company_admin"
    manager = "manager"
    staff = "staff"
    customer = "customer"


class UserStatus(StrEnum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"
