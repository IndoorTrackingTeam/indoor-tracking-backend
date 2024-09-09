from fastapi import APIRouter, HTTPException, status

from src.utils.router_data_service import convert_last_data_to_df
from src.database.repositories.router_data_repository import RouterDataDAO
from src.models.router_data import RouterData
from src.utils.converter import Message

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Insert router data to mongoDB', response_model=Message)
def create_training_data(data: RouterData):
    routerDataDAO = RouterDataDAO()
    
    status = routerDataDAO.update(data)

    if status == False:
        status = routerDataDAO.create(data)

    if status == None or status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Data created successfully')

@router.get('/get-last-data-from-esp-id', status_code=status.HTTP_200_OK)
def get_last_data_from_esp_id(esp_id: str):
    routerDataDAO = RouterDataDAO()
    
    doc = routerDataDAO.get_last_data(esp_id)

    df = convert_last_data_to_df(doc)

    dict_data = df.to_dict(orient='records')

    if doc == None or doc == False:
        raise HTTPException(status_code=500)
    
    return dict_data