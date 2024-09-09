from datetime import datetime
from src.models.hospital_settings_model import MacList
from src.database.config_db import Database

class SettingsDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='settings')

    def create_mac_list(self, macs: MacList):
        try:
            result = self.db.collection.insert_one(macs.model_dump())
            
            return result.acknowledged
        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
        
    def update_mac_list(self, macs: MacList):
        try:
            result = self.db.collection.update_one({"hospital_name": macs.hospital_name}, {
                '$set': {"macs": macs.macs}
            })
            
            return result.matched_count >= 1
        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
        
    def get_mac_list(self):
        try:
            result = self.db.collection.find_one({}, {"macs": 1, "_id": 0})

            return result.get("macs", [])
            
        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
        

    
