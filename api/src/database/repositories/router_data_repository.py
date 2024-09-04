from datetime import datetime
from src.database.config_db import Database
from src.models.router_data import RouterData

class RouterDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-data')

    def create(self, data: RouterData):
        try:
            date = datetime.now()
            date_key = date.strftime("%Y-%m-%d %H:%M:%S")

            print(date_key)

            result = self.db.collection.insert_one({
                "esp_id": data.esp_id,
                "date": {
                    date_key: [network.model_dump() for network in data.networks]
                }
            })
            return result.acknowledged

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
        
    def update(self, data: RouterData):
        try:
            date = datetime.now()
            date_key = date.strftime("%Y-%m-%d %H:%M:%S")
    
            result = self.db.collection.update_one({"esp_id": data.esp_id}, {
                '$push': {
                    f'date.{date_key}': {
                        '$each': [network.model_dump() for network in data.networks]
                    }
                }
            })
            
            return result.matched_count >= 1

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
    
