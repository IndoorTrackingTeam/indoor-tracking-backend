from src.models import UserBase, Login, UserAdmin, UserPhoto
from src.database.config_db import Database
import json
from bson import json_util 
import gridfs

class UserDAO: # DAO - Data Access Object
    def __init__(self):
        self.db = Database(collection='user')

    def get_all_users(self):
        try:
            result = self.db.collection.find()
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
            result = self.db.collection.find_one({'email': email})

            return result
        except Exception as e:
            print(f'There was an error when trying to get user: {e}')
            return None

    def login_authentication(self, user_login: Login):
        try:
            result = self.db.collection.find_one(user_login.model_dump())
            data_json = json.loads(json_util.dumps(result))

            return data_json
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
        
    # async def update_photo(self, email, encoded_contents):
    #     try:
    #         result = await self.db.collection.update_one({'email': email}, {'$set':  {'profile_image': encoded_contents.decode('utf-8')}})

    #     except Exception as e:
    #         print(f'There was an error when trying to the update user: {e}')
    #         return None
    
    