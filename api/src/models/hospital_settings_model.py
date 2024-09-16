from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MacList(BaseModel):
    hospital_name: str = Field(...)
    macs: dict = Field(...)

class Settings(MacList):
    last_trained_model: Optional[datetime] = Field(default=None)