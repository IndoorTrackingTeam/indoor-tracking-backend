import json
from fastapi import APIRouter, HTTPException, status
from bson import json_util

from src.database.repositories.router_training_data_repository import RouterTrainingDataDAO
from src.models.router_data import RouterTrainingData
from src.utils.converter import Message
from src.utils.router_data_service import convert_docs_to_df, split_data

router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_description='Insert training router data to mongoDB', response_model=Message)
def create_training_data(data: RouterTrainingData):
    routerDataDAO = RouterTrainingDataDAO()

    status = routerDataDAO.update(data)

    if status == False:
        status = routerDataDAO.create(data)

    if status == None or status == False:
        raise HTTPException(status_code=500)
    
    return Message(message='Data created successfully')

@router.get('/get-data-for-training', status_code=status.HTTP_200_OK, response_description='Get all documents and return a list with a train and test json') 
def get_all_users():
    routerDataDAO = RouterTrainingDataDAO()

    docs = routerDataDAO.get_all()

    df = convert_docs_to_df(docs)
    processed_data  = split_data(df)

    if docs == None:
        raise HTTPException(status_code=500)
    elif docs == []:
        return Message(message='No user was found')

    return processed_data