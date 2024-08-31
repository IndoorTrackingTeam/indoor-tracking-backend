from fastapi import APIRouter, HTTPException, status

from src.database.repositories.router_data_repository import RouterDataDAO
from src.models.router_data import RouterData
from src.utils import Message

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Insert router data to mongoDB', response_model=Message)
def create_training_data(data: RouterData):
    routerDataDAO = RouterDataDAO()

    creation_status = routerDataDAO.create(data)

    if creation_status == None or creation_status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Data created successfully')
