from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    event_type: str
    properties: Optional[dict] = {}
    postpone: str
