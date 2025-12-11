from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, PlainSerializer
from pydantic.alias_generators import to_camel

FormattedDatetime = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"), return_type=str)
]


class CamelCaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

class ValidatedCamelCaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True, validate_by_alias=True)
