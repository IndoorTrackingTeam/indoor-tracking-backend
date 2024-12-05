from datetime import datetime


def create_valid_equipments():
    return [
        {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "1111",
            "historic": [
                {
                    "initial_date": datetime(2024,8,5,8,0,0),
                    "room": "Room 20"
                },
                {
                    "initial_date": datetime(2024,8,7,15,34,14),
                    "room": "Clinic"
                },
                {
                    "initial_date": datetime(2024,8,7,22,12,16),
                    "room": "Room 14"
                }
            ]
        },
        {
            "name": "Defibrillator",
            "register": "PAT2222",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "2222"
        },
        {
            "name": "Infusion Pump",
            "register": "PAT3333",
            "maintenance": True,
            "c_room": "Maintenance room",
            "c_date": datetime(2024,8,8,19,54,14),
            "initial_date": datetime(2024,8,8,19,54,14),
            "esp_id": "3333"
        }
    ]
def valid_equipments_response():
    return [
        {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "",
            "esp_id": "1111",
            "image": None
        },
        {
            "name": "Defibrillator",
            "register": "PAT2222",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "",
            "esp_id": "2222",
            "image": None
        },
        {
            "name": "Infusion Pump",
            "register": "PAT3333",
            "maintenance": True,
            "c_room": "Maintenance room",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "",
            "esp_id": "3333",
            "image": None
        }
    ]

def create_valid_equipment():
    return {
            "name": "Wheelchair",
            "register": "PAT4444",
            "maintenance": False,
            "c_room": "Room 2",
            "c_date": "2024-08-08T22:46:42",
            "initial_date": "2024-08-08T19:54:14",
            "esp_id": "4444"
        }

def equipment_already_exist():
    return {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "esp_id": "1111"
        }

def response_get_one():
    return {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "2024-08-08T16:54:14-03:00",
            "esp_id": "1111",
            "image": None,
            "historic": [
                {
                    "initial_date": "2024-08-05T05:00:00-03:00",
                    "room": "Room 20"
                },
                {
                    "initial_date": "2024-08-07T12:34:14-03:00",
                    "room": "Clinic"
                },
                {
                    "initial_date": "2024-08-07T19:12:16-03:00",
                    "room": "Room 14"
                }
            ]
        }

def equipments_in_same_room():
    return [
        {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "2024-08-08T16:54:14-03:00",
            "esp_id": "1111",
            "image": None,
            "historic": [
                {
                    "initial_date": "2024-08-05T05:00:00-03:00",
                    "room": "Room 20"
                },
                {
                    "initial_date": "2024-08-07T12:34:14-03:00",
                    "room": "Clinic"
                },
                {
                    "initial_date": "2024-08-07T19:12:16-03:00",
                    "room": "Room 14"
                }
            ]
        },
        {
            "name": "Defibrillator",
            "register": "PAT2222",
            "maintenance": False,
            "c_room": "Emergency",
            "c_date": "2024-08-08T16:54:14-03:00",
            "initial_date": "2024-08-08T16:54:14-03:00",
            "esp_id": "2222",
            "historic": None,
            "image": None
        }
    ]

def valid_update_mainteinance():
    return {
        "register": "PAT2222",
        "maintenance": True
    }

def invalid_update_mainteinance():
    return {
        "register": "invalid_register",
        "maintenance": True
    }

def response_historic():
    return [
        {
            "name": "Multi Parameter Monitor",
            "register": "PAT1111",
            "historic": [
                {
                    "initial_date": "2024-08-05T05:00:00-03:00",
                    "room": "Room 20"
                },
                {
                    "initial_date": "2024-08-07T12:34:14-03:00",
                    "room": "Clinic"
                },
                {
                    "initial_date": "2024-08-07T19:12:16-03:00",
                    "room": "Room 14"
                }
            ]
        },
        {
            "name": "Defibrillator",
            "register": "PAT2222",
            "historic": None
        },
        {
            "name": "Infusion Pump",
            "register": "PAT3333",
            "historic": None
        }
    ]

def valid_update_image():
    return {
  "register": "PAT2222",
  "image": "iVBORw0KGgoAAAANSUhEUg-image-exemple-not-real"
}

def invalid_update_image():
    return {
  "register": "invalid_register",
  "image": "iVBORw0KGgoAAAANSUhEUg-image-exemple-not-real"
}