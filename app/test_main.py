import pytest
from fastapi.testclient import TestClient

from .builds.service import load_files
from .main import app

client = TestClient(app)


@pytest.fixture
def files():
    load_files()


def test_get_tasks_for_build(files):
    correct_tasks = [
        "test_task2",
        "test_task3",
        "test_task1",
        "test_task5",
        "test_task4",
        "test_task6"
    ]
    build_name = "test_build"
    response = client.post("/builds/tasks", json={
        "name": build_name
    })
    assert response.status_code == 200
    assert response.json() == correct_tasks


def test_get_tasks_for_build_wrong_build_name(files):
    build_name = "this build does not exist"
    response = client.post("/builds/tasks", json={
        "name": build_name
    })
    assert response.status_code == 400


def test_get_tasks_for_build_empty_build_name(files):
    build_name = ""
    response = client.post("/builds/tasks", json={
        "name": build_name
    })
    assert response.status_code == 400
