from typing import List
from fastapi import APIRouter, status, HTTPException, Body
from src.database.repository.equipment import EquipmentDAO
from src.models import Message, EquipmentBase, Equipment, Equipment_update, Equipment_maintenance, AllEquipmentsHistoric
from src.utils import convert_mongo_document

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
        raise HTTPException(status_code=404, detail="Equipment not found")
    if historic == None:
        raise HTTPException(status_code=500)

    return [convert_mongo_document(equipment) for equipment in historic]

@router.get("/get-equipments-by-current-room", status_code=status.HTTP_200_OK, response_description='Get equipments historic', response_model=List[Equipment])
def read_equipments_by_current_room(current_room: str):
    equipmentDAO = EquipmentDAO()
    equipments = equipmentDAO.get_equipments_by_current_room(current_room)
 
    if equipments == []:
        raise HTTPException(status_code=404, detail="There is no equipment in this room")
    if equipments == False:
        raise HTTPException(status_code=500)
    

    return [convert_mongo_document(equipment) for equipment in equipments]

@router.put("/update", status_code=status.HTTP_200_OK)
def update_equipment(update_data: Equipment_update):
    equipmentDAO = EquipmentDAO()
    update_status = equipmentDAO.update(update_data)

    if update_status == False:
        raise HTTPException(status_code=404, detail="No equipment found")
    elif update_status == None:
        raise HTTPException(status_code=500)
    
    return update_status

@router.put("/update-maintenance", status_code=status.HTTP_200_OK)
def update_maintenante_equipment(update_data: Equipment_maintenance):
    equipmentDAO = EquipmentDAO()
    update_status = equipmentDAO.update_maintenance(update_data)

    if update_status == False:
        raise HTTPException(status_code=404, detail="No equipment found")
    elif update_status == None:
        raise HTTPException(status_code=500)

    return update_status

@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_equipment(patrimonio: str):
    equipmentDAO = EquipmentDAO()
    status = equipmentDAO.delete(patrimonio)

    if status == False:
        raise HTTPException(status_code=404, detail="Equipment not found")
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return status
