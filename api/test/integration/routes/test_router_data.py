import os
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

import test.utils.mock_router_data as mock

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['router-data'].insert_one(mock.create_valid_data_for_router_data())
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

def test_get_last_data_from_esp_id_error_no_mac_list(client: TestClient) -> None:
    valid_esp_id = "1212"
    response = client.get(f'/router/data/get-last-data-from-esp-id?esp_id={valid_esp_id}')
    assert response.status_code == 406
    assert response.json()["detail"] == "You need to set your mac list first."

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_get_last_data_from_esp_id_success(mock_get_mac_list, client: TestClient):
    valid_esp_id = "1212"
    mock_get_mac_list.return_value = {"D4:EE:00:7C:2F:FD": "router1", "CC:40:00:FD:64:2D": "router2"}
    response = client.get(f'/router/data/get-last-data-from-esp-id?esp_id={valid_esp_id}')
    assert response.status_code == 200
    assert "2024-08-04 10:32:23" not in response.json()
    assert "2024-09-04 10:32:26" in response.json()

def test_get_last_data_from_esp_id_fail(client: TestClient):
    valid_esp_id = "invalid"
    response = client.get(f'/router/data/get-last-data-from-esp-id?esp_id={valid_esp_id}')
    assert response.status_code == 404
