import pymongo
import os

class Database:
    def __init__(self, collection):
        database = 'indoor_db'
        if os.getenv('ENV_QA') == "True":
            database = 'indoor_db_QA'
        self.connect(database, collection) 

    def connect(self, database, collection):
        try:
            connectionString = f"mongodb+srv://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@indoor-tracking.gf1iu9s.mongodb.net/?retryWrites=true&w=majority&appName=indoor-tracking"
            self.clusterConnection = pymongo.MongoClient(
                connectionString,
                tlsAllowInvalidCertificates=True 
            )
            self.db = self.clusterConnection[database] 
            self.collection = self.db[collection] 
            print("Conectado ao banco de dados com sucesso!")
        except Exception as e:
            print(e)
