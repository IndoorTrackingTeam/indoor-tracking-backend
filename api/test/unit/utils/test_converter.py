from src.utils.converter import parse_date, convert_mongo_document
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from zoneinfo import ZoneInfo

@pytest.fixture
def mock_doc():
    return {
        '_id': {'$oid': '60d5f30b4e1d6a4b99d8c9c7'},
        'name': 'Multi Parameter Monitor',
        'register': 'PAT1111',
        'maintenance': False,
        'c_room': 'Emergency',
        'c_date': {'$date': '2024-12-06T14:30:15.123456Z'},
        'initial_date': {'$date': '2024-12-06T14:30:15Z'},
        'esp_id': '1111',
        'image': None,
        'historic': [
            {
                'initial_date': {'$date': '2024-12-05T14:30:15Z'},
                'room': 'Room 20' 
            }
        ]
    }

def test_parse_date_valid_utc_with_milliseconds():
    date_str = "2024-12-06T14:30:15.123456Z"
    result = parse_date(date_str)
    expected = datetime(2024, 12, 6, 11, 30, 15, 123456, tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert result == expected

def test_parse_date_valid_utc_without_milliseconds():
    date_str = "2024-12-06T14:30:15Z"
    result = parse_date(date_str)
    expected = datetime(2024, 12, 6, 11, 30, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert result == expected

def test_parse_date_valid_utc_with_space():
    date_str = "2024-12-06 14:30:15"
    result = parse_date(date_str)
    expected = datetime(2024, 12, 6, 11, 30, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert result == expected

def test_parse_date_invalid_format():
    date_str = "2024-12-06 14:30:15.123"
    with pytest.raises(ValueError):
        parse_date(date_str)

def test_parse_date_invalid_utc_offset():
    date_str = "2024-12-06T14:30:15+01:00"
    with pytest.raises(ValueError):
        parse_date(date_str)

def test_convert_mongo_document(mock_doc):
    result = convert_mongo_document(mock_doc)

    assert result['id'] == '60d5f30b4e1d6a4b99d8c9c7'
    assert result['c_date'] == datetime(2024, 12, 6, 11, 30, 15, 123456, tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert result['initial_date'] == datetime(2024, 12, 6, 11, 30, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))
    assert result['historic'][0]['initial_date'] == datetime(2024, 12, 5, 11, 30, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))

def test_convert_mongo_document_missing_c_date(mock_doc):
    del mock_doc['c_date']
    result = convert_mongo_document(mock_doc)
    assert 'c_date' not in result

def test_convert_mongo_document_invalid_initial_date(mock_doc):
    mock_doc['initial_date'] = {"$date": "invalid-date"}
    with pytest.raises(ValueError):
        convert_mongo_document(mock_doc)
    
def test_convert_mongo_document_no_historic(mock_doc):
    del mock_doc['historic']
    result = convert_mongo_document(mock_doc)
    assert 'historic' not in result

@patch('src.utils.converter.parse_date')
def test_parse_date_is_called_in_convert_mongo_doc(mock_parse_date, mock_doc):
    convert_mongo_document(mock_doc)

    mock_parse_date.assert_called()