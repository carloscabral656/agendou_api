from enum import StrEnum


class CompanyStatus(StrEnum):
    active = "active"
    inactive = "inactive"
    blocked = "blocked"


class UnitStatus(StrEnum):
    active = "active"
    inactive = "inactive"
