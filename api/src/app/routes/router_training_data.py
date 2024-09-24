from fastapi import APIRouter, HTTPException, status
import itertools

from src.exceptions import DocumentNotFoundError
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
def get_data_for_training():
    routerDataDAO = RouterTrainingDataDAO()

    docs = routerDataDAO.get_all()
    
    if docs == None:
        raise HTTPException(status_code=500)
    else:
        try:

            df = convert_docs_to_df(docs)
        
            processed_data_df  = split_data(df)

            processed_data_dict = [df.to_dict(orient="records") for df in processed_data_df]

            return processed_data_dict
        except DocumentNotFoundError:
            return Message(message='You need to set your mac list first.')
        
@router.get('/get-all-macs-in-training', status_code=status.HTTP_200_OK, response_description='Get all macs found in the training collection') 
def get_macs_in_training():
    routerDataDAO = RouterTrainingDataDAO()

    docs = routerDataDAO.get_all_macs()
    
    if docs == None:
        raise HTTPException(status_code=500)
    else:
        
        return docs