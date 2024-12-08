from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
import pytest

from src.utils.equipment_service import update_equipments_location, update_database
from src.models.equipment_model import UpdateEquipmentsHistoric, UpdateEquipmentsCurrentRoom

# Apenas verificando se a requisição está sendo chamada
@patch('src.app.routes.equipment.update_equipments_location')
def test_update_equipments_position_success(mock_update_equipments_location, client: TestClient) -> None:
    response = client.post('/equipment/update-equipments-position')
    mock_update_equipments_location.assert_called_once()

    assert response.status_code == 200
