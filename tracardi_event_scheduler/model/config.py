from typing import Optional, Union
from pytimeparse import parse
from pydantic import BaseModel, validator


class Config(BaseModel):
    event_type: str
    properties: Optional[dict] = {}
    postpone: Union[str, int]

    @validator("postpone")
    def must_be_valid_postpone(cls, value):
        return parse(value)
