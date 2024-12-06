from src.database.config_db import Database
from src.models.router_data import RouterTrainingData
from datetime import datetime, timezone
import json
from bson import json_util

class RouterTrainingDataDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='router-training-data')

    def create(self, data: RouterTrainingData):
        try:
            date = datetime.now(timezone.utc)
            date_key = date.strftime("%Y-%m-%d %H:%M:%S")

            print(date_key)

            result = self.db.collection.insert_one({
                "room": data.room,
                "date": {
                    date_key: [network.model_dump() for network in data.networks]
                }
            })
            return result.acknowledged

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
        
    def update(self, data: RouterTrainingData):
        try:
            date = datetime.now(timezone.utc)
            date_key = date.strftime("%Y-%m-%d %H:%M:%S")
    
            result = self.db.collection.update_one({"room": data.room}, {
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
    
    def get_all(self):
        try:
            result = self.db.collection.find({}, {"room": 1, "date": 1, "_id": 0})
            data = json.loads(json_util.dumps(result))

            if data == []:
                return None
                        
            return data

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None
    
    def get_all_macs(self):
        try:
            pipeline = [
                # Transforma o campo 'date' (um dicionário) em um array de pares [chave, valor]
                {"$project": {"date_entries": {"$objectToArray": "$date"}}},
                # Desestrutura o array resultante de datas
                {"$unwind": "$date_entries"},
                # Desestrutura o array de roteadores dentro de cada data
                {"$unwind": "$date_entries.v"},
                # Agrupa por 'mac' e pega o primeiro 'name_router' correspondente
                {"$group": {
                    "_id": "$date_entries.v.mac",
                    "name_router": {"$first": "$date_entries.v.name_router"}
                }}
            ]

            # Executa a agregação
            result = self.db.collection.aggregate(pipeline)

            # Converte o resultado em um dicionário
            all_macs = {doc['_id']: doc['name_router'] for doc in result}

            return all_macs

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None