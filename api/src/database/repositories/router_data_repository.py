from datetime import datetime
import json
from bson import json_util

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
    
    def get_last_data(self, esp_id: str):
        try:
            pipeline = pipeline = [
                # Filtra o documento pelo esp_id específico
                {"$match": {"esp_id": esp_id}},
                
                # Transforma o campo 'date' (um dicionário) em um array de pares [chave, valor]
                {"$project": {"date_entries": {"$objectToArray": "$date"}}},
                
                # Desestrutura o array resultante de datas
                {"$unwind": "$date_entries"},
                
                # Ordena os dados por chave da data (em ordem decrescente)
                {"$sort": {"date_entries.k": -1}},
                
                # Agrupa os documentos para pegar a última data (primeira após o sort)
                {"$group": {
                    "_id": "$_id", 
                    "last_date": {"$first": "$date_entries.k"},
                    "routers": {"$first": "$date_entries.v"}
                }},
                
                # Filtro
                {"$project": {
                    "_id": 0, 
                    "last_date": 1,
                    "routers": 1
                }}
            ]

            # Executa a agregação
            result = self.db.collection.aggregate(pipeline)
            parsed_json = json.loads(json_util.dumps(result))

            return parsed_json

        except Exception as e:
            print(f'There was an error when trying to insert new data: {e}')
            return None