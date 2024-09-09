import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

import test.utils.mock_router_data as mock

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    yield db
    db['router-data'].delete_many({})
    
def test_create_router_data(client: TestClient) -> None:
    body = mock.valid_router_data()
    response = client.post('/router/data/create', json=body)
    assert response.status_code == 201

def test_create_router_data_invalid_body(client: TestClient) -> None:
    body = mock.invalid_router_data()
    response = client.post('/router/data/create', json=body)
    assert response.status_code == 422