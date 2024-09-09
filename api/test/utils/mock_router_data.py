def valid_router_training_data():
    return {
        "room": "Room 20",
        "networks": [
             {
                "mac": "34:80:D2:02:FA:C8",
                "name_router": "hospital",
                "rssi": -94,
                "esp_id": "1111"
            },
            {
                "mac": "34:82:B2:02:FA:C6",
                "name_router": "hospital-wifi",
                "rssi": -87,
                "esp_id": "1111"
            },
            {
                "mac": "12:33:C2:02:00:FA",
                "name_router": "hospital-wifi2",
                "rssi": -60,
                "esp_id": "1111"
            }
        ]
    }

def invalid_router_training_data():
    return {
        "room": "Room 20",
        "networks": [
             {
                "mac": "34:80:D2:02:FA:C8",
                "name_router": "hospital",
                "rssi": -94,
            },
            {
                "mac": "34:82:B2:02:FA:C6",
                "name_router": "hospital-wifi",
                "rssi": -87,
            },
            {
                "mac": "12:33:C2:02:00:FA",
                "name_router": "hospital-wifi2",
                "rssi": -60,
            }
        ]
    }

def valid_router_data():
    return {
            "esp_id": "1111",
            "networks": [
                {
                "mac": "34:80:D2:02:FA:C8",
                "name_router": "hospital",
                "rssi": -94
                },
                {
                "mac": "34:82:B2:02:FA:C6",
                "name_router": "hospital-wifi",
                "rssi": -87
                },
                {
                "mac": "12:33:C2:02:00:FA",
                "name_router": "hospital-wifi2",
                "rssi": -60
                }
            ]
        }

def invalid_router_data():
    return { 
            "networks": [
                {
                "mac": "34:80:D2:02:FA:C8",
                "name_router": "hospital",
                "rssi": -94
                },
                {
                "mac": "34:82:B2:02:FA:C6",
                "name_router": "hospital-wifi",
                "rssi": -87
                },
                {
                "mac": "12:33:C2:02:00:FA",
                "name_router": "hospital-wifi2",
                "rssi": -60
                }
            ]
        }
