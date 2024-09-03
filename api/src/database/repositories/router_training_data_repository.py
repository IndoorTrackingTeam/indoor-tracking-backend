from src.database.config_db import Database
from src.models.router_data import RouterTrainingData

class RouterTrainingDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-training-data')

    def create(self, data: RouterTrainingData):
        try:
            result_update = self.db.collection.update_one({"mac": data.mac}, {'$push': {'historic': {
                            "esp_id": data.esp_id,
                            "date": data.date,
                            "room": data.room,
                            "rssi": data.rssi
                        }}})

            if result_update.matched_count == 0:
                new_data = {
                    "mac": data.mac,
                    "name_router": data.name_router,
                    "historic": [
                        {
                            "esp_id": data.esp_id,
                            "date": data.date,
                            "room": data.room,
                            "rssi": data.rssi
                        }
                    ]  # Inicializando 'historic' como uma lista com o objeto
                }
                result = self.db.collection.insert_one(new_data)
            
                return result.acknowledged
            return result_update.acknowledged

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None

