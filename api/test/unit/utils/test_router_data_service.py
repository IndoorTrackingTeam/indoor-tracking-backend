import pytest
from unittest.mock import MagicMock, patch
from src.exceptions import DocumentNotFoundError
from src.utils.router_data_service import convert_docs_to_df, split_data, convert_last_data_to_df
import pandas as pd

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_convert_docs_to_df_no_mac_list(mock_get_mac_list):
    # Simulando o caso onde a lista de macs está vazia
    mock_get_mac_list.return_value = []
    
    with pytest.raises(DocumentNotFoundError, match="There isn`t a mac list."):
        convert_docs_to_df([{"room": "room1", "date": {}}])

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_convert_docs_to_df_valid_data(mock_get_mac_list):
    mock_get_mac_list.return_value = {'mac1': 'router1', 'mac2': 'router2'}

    docs = [
        {"room": "room1", "date": {"2024-10-08 21:21:29": [{"mac": "mac1", 'name_router': 'router1', "rssi": -50, 'esp_id': 'ESP32-1'}, {"mac": "mac2", 'name_router': 'router2', "rssi": -60, 'esp_id': 'ESP32-1'}]}}
    ]
    
    df = convert_docs_to_df(docs)
    assert df.shape == (1, 3)
    assert all(col in df.columns for col in ['mac1', 'mac2', 'room'])
    assert df['mac1'][0] == -50

def test_split_data():
    # Criando um DataFrame fictício
    data = {
    'mac1': [-81.0, -91.0, -72.0, -75.0],
    'mac2': [-60.0, -61.0, -83.0, -91.0],
    'mac3': [-67.0, -72.0, -89.0, -85.0],
    'mac4': [-92.0, -96.0, -70.0, -69.0],
    'room': ['room1', 'room1', 'room2', 'room2']
}
    df = pd.DataFrame(data)
    
    train_df, test_df = split_data(df)
    
    assert train_df.shape == (3, 5)
    assert test_df.shape == (1, 5)

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_convert_last_data_to_df_no_mac_list(mock_get_mac_list):
    mock_get_mac_list.return_value = []
    
    with pytest.raises(DocumentNotFoundError, match="There isn`t a mac list."):
        convert_last_data_to_df(MagicMock())
        # convert_last_data_to_df([{'dates': ['2024-12-06 00:33:07', '2024-12-06 00:32:52'], 'routers': []}])

@patch('src.utils.router_data_service.SettingsDAO.get_mac_list')
def test_convert_last_data_to_df_valid_data(mock_get_mac_list):
    mock_get_mac_list.return_value = {'00:32:00:63:24:B0': 'router1', 'D8:00:13:00:2A:B0': 'router2', 'AA:DD:44:66:22:00': 'router3'}

    doc = [
        {
            'dates': ['2024-12-06 00:33:07', '2024-12-06 00:32:52', '2024-12-06 00:32:37', '2024-12-06 00:32:22', '2024-12-06 00:32:07'], 
            'routers':[
                [{
                "mac": "00:32:00:63:24:B0",
                "name_router": "router1",
                "rssi": -63
                },
                {
                "mac": "D8:00:13:00:2A:B0",
                "name_router": "router2",
                "rssi": -72
                }], 
                [{
                "mac": "00:32:00:63:24:B0",
                "name_router": "router1",
                "rssi": -60
                },
                {
                "mac": "D8:00:13:00:2A:B0",
                "name_router": "router2",
                "rssi": -72
                }
                ], 
                [{
                "mac": "AA:DD:44:66:22:00",
                "name_router": "router3",
                "rssi": -85
                }], 
                [{
                "mac": "D8:00:13:00:2A:B0",
                "name_router": "router2",
                "rssi": -87
                },
                {
                "mac": "AA:DD:44:66:22:00",
                "name_router": "router3",
                "rssi": -74
                }
                ], 
                [{
                "mac": "AA:DD:44:66:22:00",
                "name_router": "router3",
                "rssi": -61
                }]
            ] 
        }
        ]
    
    result = convert_last_data_to_df(doc)
    
    assert '2024-12-06 00:32:52' in result
    assert isinstance(result['2024-12-06 00:33:07'], list)