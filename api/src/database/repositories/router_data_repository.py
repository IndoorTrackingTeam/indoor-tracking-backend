from datetime import datetime
import json
from bson import json_util

from src.database.config_db import Database
from src.models.router_data import RouterData
from zoneinfo import ZoneInfo

class RouterDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-data')

    def create(self, data: RouterData):
        try:
            sp_tz = ZoneInfo("America/Sao_Paulo")
            date = datetime.now(sp_tz)

            date_key = date.strftime("%Y-%m-%d %H:%M:%S")

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
            sp_tz = ZoneInfo("America/Sao_Paulo")
            date = datetime.now(sp_tz)
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
    
    def get_last_data(self, esp_id: str):
        try:
            pipeline = [
            {"$match": {"esp_id": esp_id}},
            {"$project": {"date_entries": {"$objectToArray": "$date"}}},
            {"$unwind": "$date_entries"},
            {"$sort": {"date_entries.k": -1}},
            {"$limit": 5},
            {"$group": {
                "_id": "$_id", 
                "dates": {"$push": "$date_entries.k"},
                "routers": {"$push": "$date_entries.v"}
            }},            
            {"$project": {
                "_id": 0, 
                "dates": 1,
                "routers": 1
            }}
        ]

            result = self.db.collection.aggregate(pipeline)
            parsed_json = json.loads(json_util.dumps(result))

            return parsed_json

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None