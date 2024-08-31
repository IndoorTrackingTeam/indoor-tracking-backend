def valid_router_training_data():
    return {
        "esp_id": "4444",
        "rssi": -50,
        "room": "Emergency"
    }

def invalid_router_training_data():
    return {
        "esp_id": "4444",
        "rssi": "fifty",
        "room": "Emergency"
    }
def valid_router_data():
    return {
        "esp_id": "4444",
        "rssi": -50,
    }

def invalid_router_data():
    return {
        "esp_id": "4444",
        "rssi": "fifty",
    }
