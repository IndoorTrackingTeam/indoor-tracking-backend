import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest

import test.utils.mock_hospital_settings as mock


@pytest.fixture
def delete_mac_list():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['settings'].delete_many({})

@pytest.fixture
def insert_mac_list():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['settings'].delete_many({})
    db['settings'].insert_one(mock.valid_mac_list())
    # yield db

@pytest.mark.usefixtures("delete_mac_list")
def test_create_mac_list(client: TestClient) -> None:
    body = mock.valid_mac_list()
    response = client.post('/settings/create-mac-list', json=body)
    assert response.status_code == 201

@pytest.mark.usefixtures("insert_mac_list")
def test_create_mac_list_wrong_body(client: TestClient) -> None:
    body = mock.invalid_mac_list()
    response = client.post('/settings/create-mac-list', json=body)
    assert response.status_code == 422

@pytest.mark.usefixtures("insert_mac_list")
def test_update_mac_list_success(client: TestClient) -> None:
    body = mock.valid_update_mac_list()
    response = client.put('/settings/update-mac-list', json=body)
    assert response.status_code == 200
    assert response.json()["message"] == 'List updated successfully'

@pytest.mark.usefixtures("delete_mac_list")
def test_update_mac_list_error(client: TestClient) -> None:
    body = mock.valid_update_mac_list()
    response = client.put('/settings/update-mac-list', json=body)
    assert response.status_code == 404
    assert response.json()["detail"] == "No mac list found"

@pytest.mark.usefixtures("insert_mac_list")
def test_get_mac_list_success(client: TestClient) -> None:
    response = client.get('/settings/get-mac-list')
    expected_response = {
            "34:80:D2:02:FA:C8": "wifi section A",
            "34:82:B2:02:FA:C6": "wifi section B",
            "12:33:C2:02:00:FA": "wifi section C",
            "32:45:A2:00:02:FA": "wifi section D",
            "32:33:00:00:D2:DF": "wifi section E"
        }
    assert response.status_code == 200
    assert response.json() == expected_response 

@pytest.mark.usefixtures("delete_mac_list")
def test_get_mac_list_error(client: TestClient) -> None:
    response = client.get('/settings/get-mac-list')
    assert response.status_code == 404
    assert response.json()["detail"] == "No mac list found"