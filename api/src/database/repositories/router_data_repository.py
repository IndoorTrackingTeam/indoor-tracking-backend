from src.database.config_db import Database
from src.models.router_data import RouterData

class RouterDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-data')

    def create(self, data: RouterData):
        try:
            result = self.db.collection.insert_one(data.model_dump())
            
            return result.acknowledged
        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None

