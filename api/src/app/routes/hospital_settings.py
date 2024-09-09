from fastapi import APIRouter, HTTPException, status

from src.database.repositories.hospital_settings_repository import SettingsDAO
from src.models.hospital_settings_model import MacList
from src.utils.converter import Message

router = APIRouter()

@router.post('/create-mac-list', status_code=status.HTTP_201_CREATED, response_description='Create a list of mac that can be used', response_model=Message)
def create_mac_list(macs: MacList):
    settingsDAO = SettingsDAO()
    
    status = settingsDAO.create_mac_list(macs)

    if status == None or status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Data created successfully')

@router.put("/update-mac-list", status_code=status.HTTP_200_OK, response_description='Update the mac list', response_model=Message)
def update_maintenante_equipment(macs: MacList):
    settingsDAO = SettingsDAO()
    
    status = settingsDAO.update_mac_list(macs)

    if status == False:
        raise HTTPException(status_code=404, detail="No mac list found")
    elif status == None:
        raise HTTPException(status_code=500)

    return Message(message='List updated successfully')
