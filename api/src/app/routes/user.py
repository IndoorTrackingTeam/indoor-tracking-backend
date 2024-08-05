import base64
from typing import List
from fastapi import APIRouter, File, Form, UploadFile, status, HTTPException, Body
from fastapi.responses import JSONResponse
from pydantic import Field
from src.database.repository.user import UserDAO
from src.models import UserBase, Login, UserAdmin, Message, UserData, UserPhoto

router = APIRouter()

@router.get('/read-all', status_code=status.HTTP_200_OK, response_description='Get all users', response_model=List[UserData])
def get_all_users():
    userDAO = UserDAO()
    users = userDAO.get_all_users()

    if users == None:
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

@router.post('/login', status_code=status.HTTP_200_OK, response_description='Login authentication', response_model=UserData)
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
        raise HTTPException(status_code=500, )

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
    creation_status = userDAO.update_user(update_user)

    if creation_status == False:
        raise HTTPException(status_code=404, detail='User not found')
    elif creation_status == None:        
        raise HTTPException(status_code=500)
    
    return Message(message='User updated successfully')

# @router.post("/upload-photo/")
# # async def upload_image(update_photo: UserPhoto):
# async def upload_image(email: str = Form(...), image_: UploadFile = File(...)):
#     if image_.content_type not in ["image/jpeg", "image/png"]:
#         raise HTTPException(status_code=400, detail="Invalid image format")
     
#     userDAO = UserDAO
#     # Ler o arquivo de imagem
#     # image.filename = "teste.jpg"
#     image_data = await image_.read()
#     encoded_contents = base64.b64encode(image_data)

#     filename_ = image_.filename
#     print(f'File name: {filename_}')

#     status = await userDAO.update_photo(email, encoded_contents)

#     return Message(message='Image uploaded successfully')
