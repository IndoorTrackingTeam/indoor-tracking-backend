from src.database.config_db import Database
from src.models.router_data import RouterTrainingData

class RouterTrainingDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-training-data')

    def create(self, data: RouterTrainingData):
        try:
            result_update = self.db.collection.update_one({"name": "training data"}, {'$push': {'historic': data.model_dump()}})

            if result_update.matched_count == 0:
                new_data = {
                    "name": "training data",
                    "historic": [data.model_dump()]  # Inicializando 'historic' como uma lista com o objeto
                }
                result = self.db.collection.insert_one(new_data)
            
                return result.acknowledged
            return result_update.acknowledged

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None

