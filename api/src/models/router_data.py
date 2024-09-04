from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RouterData(BaseModel):
    mac: str = Field(...)
    name_router: str = Field(...)
    esp_id: str = Field(...)
    rssi: int = Field(...)
    # date: Optional[datetime] = Field(default=datetime.now())

class RouterTrainingData(BaseModel):
    room: str = Field(...)
    networks: List[RouterData] = Field(...)


# class NewRouterTrainingData(BaseModel):
#     room: str = Field(...)
#     date: Optional[datetime] = Field(default=datetime.now())
#     linha
    
        