import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest
import test.utils.mockEquipment as mock

@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['equipment'].insert_many(mock.create_valid_equipments())
    yield db
    db['equipment'].delete_many({})
    
def test_get_all_equipments(client: TestClient) -> None:
    response = client.get('/equipment/read-all')
    expected_response = mock.valid_equipments_response()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_history_equipment(client: TestClient) -> None:
    response = client.get(f'/equipment/historic')
    expected_response = mock.response_historic()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_create_equipment(client: TestClient) -> None:
    body = mock.create_valid_equipment()
    response = client.post('/equipment/create', json=body)
    assert response.status_code == 201

def test_create_equipment_invalid_body(client: TestClient) -> None:
    body = {}
    response = client.post('/equipment/create', json=body)
    assert response.status_code == 422

def test_create_equipment_fail(client: TestClient) -> None:
    body = mock.equipment_already_exist()
    response = client.post('/equipment/create', json=body)
    assert response.status_code == 409

def test_read_one_equipment(client: TestClient) -> None:
    register = 'PAT1111'
    response = client.get(f'/equipment/read-one?register_={register}')
    expected_response = mock.response_get_one()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_read_one_equipment_fail(client: TestClient) -> None:
    register = 'invalid_register'
    response = client.get(f'/equipment/read-one?register_={register}')
    assert response.status_code == 404

def test_read_equipments_by_current_room(client: TestClient) -> None:
    current_room = 'Emergency'
    expected_response = mock.equipments_in_same_room()
    response = client.get(f'/equipment/get-equipments-by-current-room?current_room={current_room}')
    assert response.status_code == 200
    assert response.json() == expected_response

def test_update_equipment(client: TestClient) -> None:
    body = mock.valid_update_mainteinance()
    response = client.put('/equipment/update-maintenance', json=body)
    assert response.status_code == 200

def test_update_equipment_invalid_body(client: TestClient) -> None:
    body = mock.invalid_update_mainteinance()
    response = client.put('/equipment/update-maintenance', json=body)
    assert response.status_code == 404

def test_delete_equipment(client: TestClient) -> None:
    register = 'PAT1111'
    response = client.delete(f'/equipment/delete?register_={register}')
    assert response.status_code == 200

def test_delete_equipment_invalid_register(client: TestClient) -> None:
    register = 'invalid_register'
    response = client.delete(f'/equipment/delete?register_={register}')
    assert response.status_code == 404

def test_get_equipment_current_room_and_date_by_esp_id(client: TestClient) -> None:
    esp_id = '2222'
    response = client.get(f'/equipment/get-equipments-current-room-and-date?esp_id={esp_id}')
    expected_response = mock.response_current_room_date()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_equipment_current_room_and_date_by_esp_id_invalid_esp_id(client: TestClient) -> None:
    esp_id = 'invalid_esp_id'
    response = client.get(f'/equipment/get-equipments-current-room-and-date?esp_id={esp_id}')
    expected_response = mock.response_current_room_date()
    assert response.status_code == 404

def test_update_current_room(client: TestClient) -> None:
    body = mock.valid_esp_id_room()
    response = client.put(f'/equipment/update-current-room', json=body)
    assert response.status_code == 200

def test_update_current_room_invalid_esp_id(client: TestClient) -> None:
    body = mock.invalid_esp_id_room()
    response = client.put(f'/equipment/update-current-room', json=body)
    assert response.status_code == 404

def test_update_historic(client: TestClient) -> None:
    body = mock.valid_update_historic()
    response = client.put('/equipment/update-historic', json=body)
    assert response.status_code == 200

def test_update_historic_invalid_body(client: TestClient) -> None:
    body = mock.invalid_update_historic()
    response = client.put('/equipment/update-historic', json=body)
    assert response.status_code == 404

def test_update_image(client: TestClient) -> None:
    body = mock.valid_update_image()
    response = client.put('/equipment/update-image', json=body)
    assert response.status_code == 200

def test_update_image_invalid_register(client: TestClient) -> None:
    body = mock.invalid_update_image()
    response = client.put('/equipment/update-image', json=body)
    assert response.status_code == 404
    