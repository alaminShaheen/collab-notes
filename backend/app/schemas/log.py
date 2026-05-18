from datetime import datetime
from typing import Any

from pydantic import BaseModel


class LogRead(BaseModel):
    event_type: str
    user_id: int
    resource_id: str | None
    timestamp: datetime
    metadata: dict[str, Any]
