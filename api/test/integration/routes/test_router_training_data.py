import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

import test.utils.mock_router_data as mock

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['router-training-data'].insert_many(mock.create_valid_data_for_training_data())
    yield db
    db['router-training-data'].delete_many({})

def test_get_macs_in_training(client: TestClient) -> None:
    response = client.get('/router/training-data/get-all-macs-in-training')
    expected_response = {"FD:00:FF:CA:DE:D2": "router-test", "B2:CF:AA:CC:FF:00": "router-test", "AA:22:FF:22:24:00": "invalid-router", "CC:20:FF:EE:1A:00": "invalid-router"}

    assert response.status_code == 200
    assert response.json() == expected_response
    
def test_create_router_training_data(client: TestClient) -> None:
    body = mock.valid_router_training_data()
    response = client.post('/router/training-data/create', json=body)
    assert response.status_code == 201

def test_create_router_training_data_invalid_body(client: TestClient) -> None:
    body = mock.invalid_router_training_data()
    response = client.post('/router/training-data/create', json=body)
    assert response.status_code == 422

def test_get_data_for_training_error_no_mac_list(client: TestClient) -> None:
    response = client.get('/router/training-data/get-data-for-training')
    assert response.status_code == 406
    assert response.json()["detail"] == "You need to set your mac list first."

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_get_data_for_training_success(mock_get_mac_list, client: TestClient) -> None:
    mock_get_mac_list.return_value = {"FD:00:FF:CA:DE:D2": "router-test", "B2:CF:AA:CC:FF:00": "router-test"}
    response = client.get('/router/training-data/get-data-for-training')
    assert response.status_code == 200
    assert len(response.json()) == 2
    expected_keys = {"FD:00:FF:CA:DE:D2", "B2:CF:AA:CC:FF:00", "room"}
    for inner_list in response.json():
        for item in inner_list:
            assert set(item.keys()) == expected_keys