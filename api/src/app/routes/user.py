from typing import List, Union
from fastapi import APIRouter, BackgroundTasks, status, HTTPException, Body
from fastapi.responses import JSONResponse

from src.utils.user_service import send_email_background
from src.database.repositories.user_repository import UserDAO
from src.models.user_model import UserBase, Login, UserAdmin, UserData, UserId, UserBasicData, UpdateUserPhoto
from src.utils.converter import Message

router = APIRouter()

@router.get('/read-all', status_code=status.HTTP_200_OK, response_description='Get all users', response_model=Union[List[UserData], Message])
def get_all_users():
    userDAO = UserDAO()
    users = userDAO.get_all_users()

    if users == None:
        raise HTTPException(status_code=500)
    elif users == []:
        return Message(message='No user was found')

    return users

@router.get('/get-user', status_code=status.HTTP_200_OK, response_description='Get user', response_model=UserBasicData)
def get_one_users(id: str):
    userDAO = UserDAO()
    users = userDAO.get_user_by_id(id)

    if users == None:
        raise HTTPException(status_code=404, detail="User not found")
    elif users == False:
        raise HTTPException(status_code=500)

    return users

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Create a new user', response_model=Message)
def create_new_user(new_user: UserBase = Body(...)):
    userDAO = UserDAO()
    user = userDAO.get_user_by_email(new_user.email)
    if user:
        raise HTTPException(status_code=409, detail='User with this email already exists')

    creation_status = userDAO.create_user(new_user)

    if creation_status == None or creation_status == False:
        raise HTTPException(status_code=500)

    return Message(message='User created successfully')

@router.post('/login', status_code=status.HTTP_200_OK, response_description='Login authentication', response_model=UserId)
def login(user_login: Login):
    userDAO = UserDAO()
    auth_result = userDAO.login_authentication(user_login)

    if auth_result == "email_not_found":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid login", "param": "email"}
        )

    if auth_result == "incorrect_password":
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid login", "param": "password"}
        )

    if auth_result is None:
        raise HTTPException(status_code=500, detail='Internal server error')

    return auth_result


@router.post('/change-user-admin', status_code=status.HTTP_200_OK, response_description='Change user authorizations (administrator)', response_model=Message)
def change_admin(new_user_admin:UserAdmin):
    userDAO = UserDAO()
    user_updated = userDAO.change_admin(new_user_admin)

    if user_updated == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif user_updated == None:
        raise HTTPException(status_code=500)

    return Message(message='User data changed')

@router.delete('/delete', status_code=status.HTTP_200_OK, response_description='Delete user', response_model=Message)
def delete_user(user_email: str):
    userDAO = UserDAO()
    status = userDAO.delete_user(user_email)

    if status == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif status == None:        
        raise HTTPException(status_code=500)

    return Message(message='User deleted successfully')

@router.put('/update', status_code=status.HTTP_200_OK, response_description='Update user', response_model=Message)
def update_user(update_user: UserBase):
    userDAO = UserDAO()
    status = userDAO.update_user(update_user)

    if status == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='User updated successfully')

@router.put('/update-photo', status_code=status.HTTP_200_OK, response_description='Update user photo', response_model=Message)  
def update_user(update_user_photo: UpdateUserPhoto):
    userDAO = UserDAO()
    status = userDAO.update_user_photo(update_user_photo)

    if status == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='Image uploaded successfully')

@router.get('/send-email/redefine-password')
def send_email_backgroundtasks(background_tasks: BackgroundTasks, email: str):
    send_email_background(background_tasks, 'Redefinição de senha', email)

    return Message(message='Sending email')

@router.post('/redefine-password', status_code=status.HTTP_200_OK, response_description='Change user authorizations (administrator)', response_model=Message)
def change_admin(user_login: Login):
    userDAO = UserDAO()
    user_updated = userDAO.redefine_password(user_login)

    if user_updated == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif user_updated == None:
        raise HTTPException(status_code=500)

    return Message(message='User data changed')