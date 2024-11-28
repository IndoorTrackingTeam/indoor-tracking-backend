from src.models.user_model import UserBase, Login, UserAdmin, UserBasicData
from src.database.config_db import Database
import json
from bson import ObjectId, json_util 

class UserDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='user')

    def get_all_users(self):
        try:
            result = self.db.collection.find({}, {'_id': 0, 'password': 0} )
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get users: {e}')
            return None
        
    def create_user(self, new_user: UserBase):
        try:
            user_data = new_user.model_dump(by_alias=True)
            user_data['isAdmin'] = False
            result = self.db.collection.insert_one(user_data)
            
            return result.acknowledged
        except Exception as e:
            print(f'There was an error when trying to create a new user: {e}')
            return None
        
    def get_user_by_email(self, email):
        try:
            result = self.db.collection.find_one({'email': email}, {'_id': 0,'email': 1, 'name': 1, 'photo':1})
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return False

    def get_user_by_id(self, id):
        try:
            result = self.db.collection.find_one({'_id': ObjectId(id)}, {'_id': 0,'email': 1, 'name': 1, 'photo':1})
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return False
    
    def get_user_photo_by_email(self, email):
        try:
            result = self.db.collection.find_one({'email': email}, {'photo': 1})
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return False

    def login_authentication(self, user_login: Login):
        try:
            user_data = self.db.collection.find_one({'email': user_login.email}, {'_id': 1, 'password': 1})
            if not user_data:
                return 'email_not_found'

            if user_data['password'] != user_login.password:
                return 'incorrect_password'

            data_json = json.loads(json_util.dumps(user_data))
            return {'_id': data_json['_id']['$oid']}

        except Exception as e:
            print(f'There was an error trying to authenticate the user: {e}')
            return None
    
    def change_admin(self, user_admin: UserAdmin):
        try:
            result = self.db.collection.update_one({'email': user_admin.email}, {'$set': {'isAdmin': user_admin.isAdmin}})

            if result.modified_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to change user: {e}')
            return None
    
    def delete_user(self, email):
        try:
            result = self.db.collection.delete_one({'email': email})

            if result.deleted_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error when trying to delete the user: {e}')
            return None
        
    def update_user(self, data_user: UserBase):
        try:
            result = self.db.collection.update_one({'email': data_user.email}, {'$set':  data_user.model_dump()})

            if result.modified_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error when trying to the update user: {e}')
            return None

    def update_user_photo(self, data_user: UserBasicData):
        try:
            result = self.db.collection.update_one({'_id': ObjectId(data_user.id)}, {'$set':  {'photo': data_user.photo}})

            if result.modified_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error when trying to the update user: {e}')
            return None
        
    def redefine_password(self, user_login: Login):
        try:
            result = self.db.collection.update_one({'email': user_login.email}, {'$set': {'password': user_login.password}})

            if result.matched_count == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f'There was an error trying to change user: {e}')
            return None
    
    def get_users_emails(self):
        try:
            result = self.db.collection.find({}, {'_id': 0, 'email': 1})
            data_json = json.loads(json_util.dumps(result))

            return data_json
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return False
    
    