from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    name: str
    email: str
    id: UUID | None = None
