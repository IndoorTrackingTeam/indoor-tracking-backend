
def create_valid_users():
    return [
        {"email": "jake@email.com", "name": "Jake Woody", "password": "123456"},
        {"email": "jessica@email.com", "name": "Jessica Prince", "password": "123456"},
        {"email": "emma@email.com", "name": "Emma France", "password": "123456"}
    ]

def response_get_one():
    return {
        "email": "jake@email.com", 
        "name": "Jake Woody",
        "photo": "" 
    }
def response_create_valid_users():
    return [
        {"email": "jake@email.com", "name": "Jake Woody", "isAdmin": False, "photo": ""},
        {"email": "jessica@email.com", "name": "Jessica Prince", "isAdmin": False, "photo": ""},
        {"email": "emma@email.com", "name": "Emma France", "isAdmin": False, "photo": ""}
    ]

def valid_user():
    return {
        "name": "Bob Dylan",
        "email": "bo@email.com",
        "password": "123456"
    }

def user_already_exist():
    return {
        "name": "Jake Woody",
        "email": "jake@email.com",
        "password": "123456"
    }

def valid_login():
    return {
        "email": "jake@email.com",
        "password": "123456"
    }

def invalid_email_login():
    return {
        "email": "invalid@email.com",
        "password": "123456"
    }
def invalid_password_login():
    return {
        "email": "jake@email.com",
        "password": "pass123"
    }

def valid_user_change_admin():
    return {
        "email": "jake@email.com",
        "isAdmin": True
    }

def valid_user_change_admin_fail():
    return {
        "email": "invalid@email.com",
        "isAdmin": True
    }

def valid_user_update():
    return {
        "name": "Jessica Summer Prince",
        "email": "jessica@email.com",
        "password": "123456"
    }

def invalid_user_update():
    return {
        "name": "Jessica Summer Prince",
        "email": "invalid@email.com",
        "password": "123456"
    }

def invalid_update_photo():
    return {
  "_id": "66d1cd3699dd1572552651dd",
  "photo": "iVBORw0KGgoAAAANSUhEUg-photo-exemple-not-real"
}

def valid_login_for_redefine_password():
    return {
        "email": "jake@email.com",
        "password": "newpassword123"
    }

def invalid_login_for_redefine_password():
    return {
        "email": "invalid@email.com",
        "password": "newpassword123"
    }