from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RouterData(BaseModel):
    esp_id: str = Field(...)
    rssi: int = Field(...)
    date: Optional[datetime] = Field(default=datetime.now())

class RouterTrainingData(RouterData):
    room: str = Field(...)
        