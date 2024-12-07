from typing import List
from fastapi import APIRouter, status, HTTPException, Body
from src.utils.equipment_service import update_equipments_location
from src.database.repositories.equipment_repository import EquipmentDAO
from src.models.equipment_model import EquipmentBase, Equipment, EquipmentMaintenance, AllEquipmentsHistoric, UpdateImage, UpdateEquipments
from src.utils.converter import Message, convert_mongo_document

router = APIRouter()

@router.get("/read-all", status_code=status.HTTP_200_OK, response_description='Get all equipment', response_model=List[EquipmentBase])
def get_all_equipments():
    equipmentDAO = EquipmentDAO()
    equipments = equipmentDAO.get_all()

    if equipments == None:
        raise HTTPException(status_code=500)
    
    equipments = [convert_mongo_document(equipment) for equipment in equipments]
    
    return equipments

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create a new user', response_model=Message)
def create_equipment(new_equipment: EquipmentBase):
    equipmentDAO = EquipmentDAO()
    equipment_exist = equipmentDAO.read_one(new_equipment.register_)
    if equipment_exist:
        raise HTTPException(status_code=409, detail="Equipment with this patrimony already exists")
    creation_status = equipmentDAO.create(new_equipment)

    if creation_status == None or creation_status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Equipment created successfully')

@router.get("/read-one", status_code=status.HTTP_200_OK, response_description='Read equipment', response_model=Equipment)
def read_one_equipment(register_: str):
    equipmentDAO = EquipmentDAO()
    equipment = equipmentDAO.read_one(register_)

    if equipment == None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    if equipment == False:
        raise HTTPException(status_code=500)

    equipment = convert_mongo_document(equipment)

    return equipment

@router.get("/historic", status_code=status.HTTP_200_OK, response_description='Get equipments historic', response_model=List[AllEquipmentsHistoric])
def history_equipment():
    equipmentDAO = EquipmentDAO()
    historic = equipmentDAO.get_historic()

    if historic == []:
        raise HTTPException(status_code=404, detail="No equipment found")
    if historic == None:
        raise HTTPException(status_code=500)

    return [convert_mongo_document(equipment) for equipment in historic]

@router.get("/get-equipments-by-current-room", status_code=status.HTTP_200_OK, response_description='Get specific equipment', response_model=List[Equipment])
def read_equipments_by_current_room(current_room: str):
    equipmentDAO = EquipmentDAO()
    equipments = equipmentDAO.get_equipments_by_current_room(current_room)
 
    if equipments == []:
        raise HTTPException(status_code=404, detail="There is no equipment in this room")
    if equipments == False:
        raise HTTPException(status_code=500)

    return [convert_mongo_document(equipment) for equipment in equipments]

@router.put("/update-maintenance", status_code=status.HTTP_200_OK, response_description='Updates equipment maintenance', response_model=Message)
def update_maintenante_equipment(update_data: EquipmentMaintenance):
    equipmentDAO = EquipmentDAO()
    update_status = equipmentDAO.update_maintenance(update_data)

    if update_status == False:
        raise HTTPException(status_code=404, detail="No equipment found")
    elif update_status == None:
        raise HTTPException(status_code=500)

    return Message(message='Equipment updated successfully')

@router.delete("/delete", status_code=status.HTTP_200_OK, response_description='Delete equipment', response_model=Message)
def delete_equipment(register_: str):
    equipmentDAO = EquipmentDAO()
    status = equipmentDAO.delete(register_)

    if status == False:
        raise HTTPException(status_code=404, detail="Equipment not found")
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='Equipment deleted successfully')

@router.put('/update-image', status_code=status.HTTP_200_OK, response_description='Update equipment photo', response_model=Message)  
def update_image(update_equipment_image: UpdateImage):
    equipmentDAO = EquipmentDAO()
    status = equipmentDAO.update_equipment_image(update_equipment_image)

    if status == False:
        raise HTTPException(status_code=404, detail='Equipment not found')
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='Image uploaded successfully')

@router.put('/update', status_code=status.HTTP_200_OK, response_description='Update equipment', response_model=Message)  
def update_equipment_(update_equipment: UpdateEquipments):
    equipmentDAO = EquipmentDAO()
    status = equipmentDAO.update(update_equipment)

    if status == False:
        raise HTTPException(status_code=404, detail='Equipment not found')
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='Updated Equipments successfully')

@router.post('/update-equipments-position', status_code=status.HTTP_200_OK, response_description='Update equipments position', response_model=Message)  
async def update_equipments_position():
    try:
        await update_equipments_location()
        return Message(message="Updated equipments position successfully")
                
    except Exception as e:
        Message(message=f'Error when updating equipments position: {e}')

