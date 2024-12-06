import os
from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest
import test.utils.mockUser as mock
 
@pytest.fixture(scope="session", autouse=True)
def config_mongo():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['user'].insert_many(mock.create_valid_users())
    yield db
    db['user'].delete_many({})

@pytest.fixture(scope="function", autouse=False)
def get_user_id():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    user = db['user'].find_one({"email": "jake@email.com"}, {"_id": 1})
    id = str(user["_id"])
    return id

@pytest.fixture
def delete_all_users():
    client = MongoClient(os.getenv('DB_URL'), tlsAllowInvalidCertificates=True)
    db = client['indoor_db_QA']  # Collection específica para testes
    db['user'].delete_many({})

def test_read_all(client: TestClient) -> None:
    response = client.get('/user/read-all')
    expected_response = mock.response_create_valid_users()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user(client: TestClient, get_user_id) -> None:
    valid_id = get_user_id
    response = client.get(f'/user/get-user?id={valid_id}')
    expected_response = mock.response_get_one()
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_user_fail(client: TestClient) -> None:
    invalid_id = "66d1cd3699dd1572552651dd"
    response = client.get(f'/user/get-user?id={invalid_id}')
    assert response.status_code == 404

def test_create_new_user(client: TestClient) -> None:
    body = mock.valid_user()
    response = client.post("/user/create", json=body)
    assert response.status_code == 201

def test_create_new_user_wrong_body(client: TestClient) -> None:
    body = {}
    response = client.post("/user/create", json=body)
    assert response.status_code == 422

def test_create_new_user_missing_field(client: TestClient) -> None:
    body = mock.create_user_but_missing_field()
    response = client.post("/user/create", json=body)
    assert response.status_code == 422

def test_create_new_user_fail(client: TestClient) -> None:
    body = mock.user_already_exist()
    response = client.post("/user/create", json=body)
    assert response.status_code == 409

def test_login_valid(client: TestClient) -> None:
    body = mock.valid_login()
    response = client.post("/user/login", json=body)
    assert response.status_code == 200

def test_login_invalid_email(client: TestClient) -> None:
    body = mock.invalid_email_login()
    response = client.post("/user/login", json=body)
    assert response.status_code == 401
    assert response.json()["param"] == "email"

def test_login_invalid_password(client: TestClient) -> None:
    body = mock.invalid_password_login()
    response = client.post("/user/login", json=body)
    assert response.status_code == 401
    assert response.json()["param"] == "password"

def test_changeAdmin(client: TestClient) -> None:
    body = mock.valid_user_change_admin()
    response = client.post("/user/change-user-admin", json=body)
    assert response.status_code == 200

def test_changeAdmin_fail(client: TestClient) -> None:
    body = mock.valid_user_change_admin_fail()
    response = client.post("/user/change-user-admin", json=body)
    assert response.status_code == 404

def test_update_user(client: TestClient) -> None:
    body = mock.valid_user_update()
    response = client.put("/user/update", json=body)
    assert response.status_code == 200

def test_update_user_fail(client: TestClient) -> None:
    body = mock.invalid_user_update()
    response = client.put("/user/update", json=body)
    assert response.status_code == 404

def test_deleteUser(client: TestClient) -> None:
    valid_email = "emma@email.com"
    response = client.delete(f"/user/delete?user_email={valid_email}")
    assert response.status_code == 200

def test_deleteUser_fail(client: TestClient) -> None:
    invalid_email = "invalid@email.com"
    response = client.delete(f"/user/delete?user_email={invalid_email}")
    assert response.status_code == 404

def test_update_photo(client: TestClient, get_user_id) -> None:
    body = {
        "_id": get_user_id,
        "photo": "iVBORw0KGgoAAAANSUhEUg-photo-exemple-not-real"
    }
    response = client.put('/user/update-photo', json=body)
    assert response.status_code == 200

def test_update_photo_invalid_register(client: TestClient) -> None:
    body = mock.invalid_update_photo()
    response = client.put('/user/update-photo', json=body)
    assert response.status_code == 404

def test_send_email_backgroundtasks_success(client: TestClient) -> None:
    valid_email = "jake@email.com"
    response = client.get(f'/user/send-email/redefine-password?email={valid_email}')
    assert response.status_code == 202
    assert response.json()["message"] == "Sending email"

def test_send_email_backgroundtasks_invalid_email(client: TestClient) -> None:
    invalid_email = "invalid@email.com"
    response = client.get(f'/user/send-email/redefine-password?email={invalid_email}')
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_redefine_password(client: TestClient) -> None:
    body = mock.valid_login_for_redefine_password()
    response = client.put("/user/redefine-password", json=body)
    assert response.status_code == 200
    assert response.json()["message"] == "User data changed"

def test_redefine_password_invalid_email(client: TestClient) -> None:
    body = mock.invalid_login_for_redefine_password()
    response = client.put("/user/redefine-password", json=body)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.usefixtures("delete_all_users")
def test_read_all_no_user_found(client: TestClient) -> None:
    response = client.get('/user/read-all')
    assert response.status_code == 200
    assert response.json() == {"message": "No user was found"}