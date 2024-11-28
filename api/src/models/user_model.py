from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from fastapi import UploadFile, File
from datetime import datetime

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

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

class NotificationBody(BaseModel):
    equipment_name: str = Field(...)
    register_: str = Field(...)
    date: datetime = Field(...)
    location: str = Field(...)
