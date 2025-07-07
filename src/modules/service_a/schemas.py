from pydantic import BaseModel, Field, PositiveInt
from typing import Optional, List


class EquipmentID(BaseModel):
    id: str = Field(pattern=r"^[a-zA-Z0-9]{6,}$")


class MyParameter(BaseModel):
    username: str = Field(alias='username', max_length=10, )
    password: str = Field(alias='password', max_length=10, )
    vlan: Optional[int] = Field(alias='vlan', default=None, )
    interfaces: List[PositiveInt] = Field(alias='interfaces', max_length=4, )


class CpeUpdate(BaseModel):
    timeout_in_seconds: PositiveInt
    parameters: MyParameter
