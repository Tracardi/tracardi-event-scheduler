import json
from json import JSONDecodeError
from typing import Optional, Union
from pytimeparse import parse
from pydantic import BaseModel, validator


class Config(BaseModel):
    event_type: str
    properties: Union[str, dict] = "{}"
    postpone: Union[str, int]

    @validator("postpone")
    def must_be_valid_postpone(cls, value):
        return parse(value)

    @validator("properties")
    def must_be_json(cls, value):
        try:
            return json.loads(value)
        except JSONDecodeError as e:
            raise ValueError(str(e))

