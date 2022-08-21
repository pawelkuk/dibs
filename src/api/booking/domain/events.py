from dataclasses import dataclass
from uuid import UUID

class Event:
    pass

@dataclass
class ScreeningChanged:
    screening_id: UUID
