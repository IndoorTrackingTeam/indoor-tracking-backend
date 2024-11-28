from src.database.config_db import Database
from datetime import datetime
import json
from bson import json_util
from src.models.equipment_model import EquipmentBase, EquipmentMaintenance, UpdateEquipmentsCurrentRoom, UpdateEquipmentsHistoric, UpdateImage

class EquipmentDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='equipment')

    def get_all(self):
        try:
            res = self.db.collection.find({}, {'_id': 0, 'name': 1,'register': 1, 'maintenance': 1, 'c_room': 1, 'c_date': 1, 'esp_id': 1, "image": 1} )

            parsed_json = json.loads(json_util.dumps(res))
            return parsed_json
        
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return None
    
    def create(self, new_equipment: EquipmentBase):
        try:
            result = self.db.collection.insert_one(new_equipment.model_dump(by_alias=True))
            
            return result.acknowledged
        except Exception as e:
            print(f'There was an error trying to create the equipment: {e}')
            return None

    def read_one(self, register):
        try:
            res = self.db.collection.find_one({'register': register})
            print('one equipment: ', res)

            parsed_json = json.loads(json_util.dumps(res))

            return parsed_json
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return False
        
    def get_equipments_by_current_room(self, current_room):
        try:
            res = self.db.collection.find({'c_room': current_room})

            parsed_json = json.loads(json_util.dumps(res))
            print(f"get equip by c room: {parsed_json}")

            return parsed_json
        except Exception as e:
            print(f'There was an error trying to get the equipment by current room: {e}')
            return False
        
    # def update(self, data_equipment):
    #     try:
    #         res = self.db.collection.update_one({'register_': data_equipment.register_}, {'$set':  {'name': data_equipment.name, 'last_maintenance': data_equipment.last_maintenance, 'next_maintenance': data_equipment.next_maintenance}})

    #         if res.matched_count == 0:
    #             return False
    #         else:
    #             return True
    #     except Exception as e:
    #         print(f'Houve um erro ao tentar pegar os equipamentos: {e}')
    #         return None
        
    def delete(self, register_):
        try:
            res = self.db.collection.delete_one({'register': register_})

            if res.deleted_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to delete the equipment: {e}')
            return None
        
    def get_historic(self):
        try:
            res = self.db.collection.find({}, {'_id': 0, 'name': 1,'register': 1, 'historic': 1})

            parsed_json = json.loads(json_util.dumps(res))
            
            return parsed_json
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return None
        
    def update_maintenance(self, data_equipment: EquipmentMaintenance):
        try:
            res = self.db.collection.update_one({'register': data_equipment.register_}, {'$set':  {'maintenance': data_equipment.maintenance}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment maintenance: {e}')
            return None
        
    def update_equipment_image(self, data: UpdateImage):
        try:
            result = self.db.collection.update_one({'register': data.register_}, {'$set':  {'image': data.image}})

            if result.modified_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error when trying to the upload image to equipment: {e}')
            return None
        
    def get_all_esp_id(self):
        try:
            res = self.db.collection.find({}, {'_id': 0, 'esp_id': 1} )

            parsed_json = json.loads(json_util.dumps(res))
            return parsed_json
        
        except Exception as e:
            print(f'There was an error trying to get the equipment: {e}')
            return None
        
    def get_current_room_and_date(self, esp_id):
        try:
            res = self.db.collection.find_one({'esp_id': esp_id},  {'_id': 0, 'name': 1, 'register': 1,  'c_room': 1, 'initial_date': 1})
            parsed_json = json.loads(json_util.dumps(res))
            
            return parsed_json
        except Exception as e:
            print(f'There was an error trying to get equipment: {e}')
            return None
        
        
    def update_historic(self, equipment_data: UpdateEquipmentsHistoric):
        try:
            res = self.db.collection.update_one({'esp_id': equipment_data.esp_id}, {'$push': {'historic': equipment_data.model_dump(exclude='esp_id')}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment maintenance: {e}')
            return None
        
    
    def update_current_room(self, equipment_data: UpdateEquipmentsCurrentRoom, date):
        try:
            res = self.db.collection.update_one({'esp_id': equipment_data.esp_id},{'$set': {'c_room': equipment_data.c_room, 'initial_date': date}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment\'s current room: {e}')
            return None
    
    def update_current_date(self, esp_id: str):
        try:
            date = datetime.now()

            res = self.db.collection.update_one({'esp_id': esp_id},{'$set': {'c_date': date}})

            if res.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to update equipment\'s current data(last time updated): {e}')
            return None
    
