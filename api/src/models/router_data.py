from typing import List, Optional
from pydantic import BaseModel, Field


class NetworksRouterTrainingData(BaseModel):
    mac: str = Field(...)
    name_router: str = Field(...)
    rssi: int = Field(...)
    esp_id: str = Field(...)

class RouterTrainingData(BaseModel):
    room: str = Field(...)
    networks: List[NetworksRouterTrainingData] = Field(...)

class NetworksRouterData(BaseModel):
    mac: str = Field(...)
    name_router: str = Field(...)
    rssi: int = Field(...)

class RouterData(BaseModel):
    esp_id: str = Field(...)
    networks: List[NetworksRouterData] = Field(...)
