import os

from typing import Generator
from fastapi.testclient import TestClient
import pytest
from main import api

# Fixture para configurar o ambiente de QA
@pytest.fixture(scope="session", autouse=True)
def set_qa_environment():
    os.environ['DB_NAME'] = "indoor_db_QA"
    
# Fixture para instanciar um cliente
@pytest.fixture(scope="function", autouse=True)
def client() -> Generator:
    with TestClient(api) as client:
        yield client

