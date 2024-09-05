import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

import test.utils.mock_hospital_settings as mock

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    yield db
    db['settings'].delete_many({})
    
def test_create_mac_list(client: TestClient) -> None:
    body = mock.valid_mac_list()
    response = client.post('/settings/create-mac-list', json=body)
    assert response.status_code == 201

def test_create_mac_list_wrong_body(client: TestClient) -> None:
    body = mock.invalid_mac_list()
    response = client.post('/settings/create-mac-list', json=body)
    assert response.status_code == 422
