def valid_mac_list():
    return {
        "hospital_name": "hospital test",
        "macs": {
            "34:80:D2:02:FA:C8": "wifi section A",
            "34:82:B2:02:FA:C6": "wifi section B",
            "12:33:C2:02:00:FA": "wifi section C",
            "32:45:A2:00:02:FA": "wifi section D",
            "32:33:00:00:D2:DF": "wifi section E"
        }
    }

def invalid_mac_list():
    return {
        "macs": {
            "34:80:D2:02:FA:C8": "wifi section A",
            "34:82:B2:02:FA:C6": "wifi section B",
            "12:33:C2:02:00:FA": "wifi section C",
            "32:45:A2:00:02:FA": "wifi section D",
            "32:33:00:00:D2:DF": "wifi section E"
        }
    }