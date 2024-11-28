from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class EquipmentBase(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    maintenance: bool = Field(default=False)
    c_room: str = Field(...)
    c_date: datetime = Field(...)
    initial_date: Optional[datetime] = Field(default=None)
    esp_id: str = Field(...)
    image: Optional[str] = Field(default=None)
    # esp_id: Optional[str] = Field(default=None)

class EquipmentHistoric(BaseModel):
    initial_date: datetime = Field(...)
    room: str = Field(...)

class Equipment(EquipmentBase):
    historic: Optional[List[EquipmentHistoric]] = Field(default=None)

class AllEquipmentsHistoric(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    historic: Optional[List[EquipmentHistoric]] = Field(default=None)

class EquipmentMaintenance(BaseModel):
    register_: str = Field(alias="register")
    maintenance: bool = Field(default=False)

class UpdateImage(BaseModel):
    register_: str = Field(alias="register")
    image: str = Field(...)

class EquipmentCurrentDateAndRoom(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    c_room: str = Field(...)
    c_date: datetime = Field(...)

class UpdateEquipmentsHistoric(BaseModel):
    esp_id: str = Field(...)
    room: str = Field(...)
    initial_date: datetime = Field(...)

class UpdateEquipmentsCurrentRoom(BaseModel):
    esp_id: str = Field(...)
    c_room: str = Field(...)