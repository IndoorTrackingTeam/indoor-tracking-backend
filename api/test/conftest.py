import os

from typing import Generator
from fastapi.testclient import TestClient
import pytest
from pymongo import MongoClient
from main import api
from test.utils.mockUser import create_valid_users
from test.utils.mockEquipment import create_valid_equipments

# Fixture para configurar o ambiente de QA
@pytest.fixture(scope="session", autouse=True)
def set_qa_environment():
    os.environ['ENV_QA'] = "True"
    
# Fixture para instanciar um cliente
@pytest.fixture(scope="function", autouse=True)
def client() -> Generator:
    with TestClient(api) as client:
        yield client

