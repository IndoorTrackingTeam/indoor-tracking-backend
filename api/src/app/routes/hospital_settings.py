from fastapi import APIRouter, HTTPException, status

from src.database.repositories.hospital_settings_repository import SettingsDAO
from src.models.hospital_settings_model import MacList
from src.utils import Message

router = APIRouter()

@router.post('/create-macs', status_code=status.HTTP_201_CREATED, response_description='Create a list of mac that can be used', response_model=Message)
def create_mac_list(macs: MacList):
    settingsDAO = SettingsDAO()
    
    status = settingsDAO.create_mac_list(macs)

    if status == None or status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Data created successfully')
