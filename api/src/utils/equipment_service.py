from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import requests

from src.models.equipment_model import UpdateEquipmentsCurrentRoom, UpdateEquipmentsHistoric
from src.database.repositories.equipment_repository import EquipmentDAO


def update_database(equipmentDAO, new_current_room, esp_id, num_try):
    num_try += 1
    try:
        sp_tz = ZoneInfo("America/Sao_Paulo")

        date = datetime.now(sp_tz)
        date_key = date.strftime("%Y-%m-%d %H:%M:%S")

        equipmentDAO.update_historic(UpdateEquipmentsHistoric(esp_id = esp_id, room = new_current_room, initial_date = date_key))
        equipmentDAO.update_current_room(UpdateEquipmentsCurrentRoom(esp_id = esp_id, c_room = new_current_room), date_key)
            
    except Exception as e:
        print(f"Error when connecting with database: {e}")