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
def create_valid_data_for_router_data():
    return {
        "esp_id": "1212",
        "date": {
            "2024-08-04 10:32:23": [{
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -83
            }, {
                "mac": "D4:EE:00:7C:2F:FD",
                "name_router": "router2",
                "rssi": -36
            }],
            "2024-09-04 10:20:30": [{
                "mac": "D4:EE:00:7C:2F:FD",
                "name_router": "router2",
                "rssi": -39
            }, {
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -82
            }],
            "2024-09-04 10:31:44": [{
                "mac": "D4:EE:00:7C:2F:FD",
                "name_router": "router2",
                "rssi": -38
            }, {
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -84
            }],
            "2024-09-04 10:31:58": [{
                "mac": "D4:EE:00:7C:2F:FD",
                "name_router": "router2",
                "rssi": -37
            }, {
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -85
            }],
            "2024-09-04 10:32:12": [{
                "mac": "D4:EE:00:7C:2F:FD",
                "name_router": "router2",
                "rssi": -39
            }, {
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -85
            }],
            "2024-09-04 10:32:26": [{
                "mac": "D4:EE:00:7C:2F:FD",  
                "name_router": "router2",
                "rssi": -37
            }, {
                "mac": "CC:40:00:FD:64:2D",
                "name_router": "router1",
                "rssi": -83
			    
		    }]
	    }
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


def create_valid_data_for_training_data():
    return [
        {
            "room": "Sala A",
            "date": {
                "2024-10-08 21:21:29": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -60,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -88,
                    "esp_id": "ESP32-1"
                }],
                "2024-10-08 21:21:42": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -69,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -85,
                    "esp_id": "ESP32-1"
                }],
                "2024-10-08 21:22:27": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -63,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -71,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "AA:22:FF:22:24:00",
                    "name_router": "invalid-router",
                    "rssi": -83,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "CC:20:FF:EE:1A:00",
                    "name_router": "invalid-router",
                    "rssi": -89,
                    "esp_id": "ESP32-1"
                }]
            }
        },
        {
            "room": "Sala B",
            "date": {
                "2024-10-08 21:30:29": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -80,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -68,
                    "esp_id": "ESP32-1"
                }],
                "2024-10-08 21:31:42": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -89,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -65,
                    "esp_id": "ESP32-1"
                }],
                "2024-10-08 21:32:27": [{
                    "mac": "FD:00:FF:CA:DE:D2",
                    "name_router": "router-test",
                    "rssi": -83,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "B2:CF:AA:CC:FF:00",
                    "name_router": "router-test",
                    "rssi": -34,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "AA:22:FF:22:24:00",
                    "name_router": "invalid-router",
                    "rssi": -60,
                    "esp_id": "ESP32-1"
                }, {
                    "mac": "CC:20:FF:EE:1A:00",
                    "name_router": "invalid-router",
                    "rssi": -63,
                    "esp_id": "ESP32-1"
                }]
            }
        },

        ]