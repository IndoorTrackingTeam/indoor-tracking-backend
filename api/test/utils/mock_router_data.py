def valid_router_training_data():
    return {
        "mac": "34:80:D2:02:FA:C8",
        "esp_id": "4444",
        "rssi": -50,
        "room": "Emergency"
    }

def invalid_router_training_data():
    return {
        "mac": "34:80:D2:02:FA:C8",
        "esp_id": "4444",
        "rssi": "fifty",
        "room": "Emergency"
    }
def valid_router_data():
    return {
        "mac": "34:80:D2:02:FA:C8",
        "esp_id": "4444",
        "rssi": -50,
    }

def invalid_router_data():
    return {
        "mac": "34:80:D2:02:FA:C8",
        "esp_id": "4444",
        "rssi": "fifty",
    }
