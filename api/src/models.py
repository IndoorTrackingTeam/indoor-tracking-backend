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

class Login(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

class UserId(BaseModel):
    id: str = Field(alias="_id", default=None)

class UserAdmin(BaseModel):
    email: str = Field(...)
    isAdmin: bool = Field(default=False)

class UserBasicData(BaseModel):
    email: Optional[str] = Field(default='')
    name: Optional[str] = Field(default='')
    photo: Optional[str] = Field(default='')
    # image: UploadFile = File(...)

class UserData(UserBasicData):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    isAdmin: bool = Field(default=False)

class UpdateUserPhoto(UserId):
    photo: str = Field(...)


class EquipmentBase(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    maintenance: bool = Field(default=False)
    c_room: str = Field(...)
    c_date: datetime = Field(...)
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

class UpdateImage(BaseModel):
    register_: str = Field(alias="register")
    image: str = Field(...)