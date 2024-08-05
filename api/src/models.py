from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from fastapi import UploadFile, File
from datetime import datetime

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

# Generic message
class Message(BaseModel):
    message: str

# User shared properties
class UserBase(BaseModel):
     name: str = Field(...)
     email: str = Field(...)
     password: str = Field(...)
    #  model_config = ConfigDict(
    #     # populate_by_name=True, # precisa disso?
    #     arbitrary_types_allowed=True, # precisa disso
    #     json_schema_extra={
    #         "example": {"name": "Frida Gilbert",
    #                      "email": "frida_gilbert@gmail.com",
    #                      "password": "12345678",
    #                      "register": "1212",
    #                      "maintenance": False}
    #     },
    # )

class UserData(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    isAdmin: bool = Field(default=False)

class Login(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class UserAdmin(BaseModel):
    email: str = Field(...)
    isAdmin: bool = Field(default=False)

class UserPhoto(BaseModel):
    email: str = Field(...)
    image: UploadFile = File(...)


class EquipmentBase(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    maintenance: bool = Field(default=False)
    last_maintenance: Optional[datetime] = Field(default=None)
    next_maintenance: Optional[datetime] = Field(default=None)
    c_room: str = Field(...)
    c_date: datetime = Field(...)
    esp_id: str = Field(...)

class EquipmentHistoric(BaseModel):
    initial_date: datetime = Field(...)
    room: str = Field(...)

class Equipment(EquipmentBase):
    historic: Optional[List[EquipmentHistoric]] = Field(default=None)
    esp_id: Optional[str] = Field(default=None)

class AllEquipmentsHistoric(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    historic: Optional[List[EquipmentHistoric]] = Field(default=None)

class EquipmentMaintenance(BaseModel):
    register_: str = Field(alias="register")
    maintenance: bool = Field(default=False)

class EquipmentCurrentDateAndRoom(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    c_room: str = Field(...)
    c_date: datetime = Field(...)

class UpdateEquipmentsHistoric(BaseModel):
    esp_id: str = Field(...)
    room: str = Field(...)
    date: datetime = Field(...)

class UpdateEquipmentsCurrentRoom(BaseModel):
    esp_id: str = Field(...)
    room: str = Field(...)
