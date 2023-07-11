import pytest
from fastapi.testclient import TestClient

from .builds.file_manager import MockBuildsFileManager
from .builds.service import load_files
from .builds.typings import AdjacencyList
from .main import app

client = TestClient(app)


@pytest.fixture
def load_test_files():
    load_files(MockBuildsFileManager())

    def fixture(
        tasks: AdjacencyList | None = None, builds: AdjacencyList | None = None
    ):
        file_manager = MockBuildsFileManager(
            tasks_adj_list=tasks, builds_adj_list=builds
        )
        load_files(file_manager)

    return fixture


def test_get_tasks_for_build(load_test_files):
    correct_tasks = [
        "test_task2",
        "test_task3",
        "test_task1",
        "test_task5",
        "test_task4",
        "test_task6",
    ]
    build_name = "test_build"
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 200
    assert response.json() == correct_tasks


def test_get_tasks_for_build_wrong_build_name(load_test_files):
    build_name = "this build does not exist"
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 400


def test_get_tasks_for_build_empty_build_name(load_test_files):
    build_name = ""
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 400


def test_get_tasks_for_build_with_unknown_task(load_test_files):
    build_name = "test_build"
    builds = {
        build_name: [
            "test_task1",
            "test_task999",
        ]
    }
    load_test_files(builds=builds)
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 422


def test_get_tasks_for_build_with_empty_tasks(load_test_files):
    build_name = "test_build"
    builds = {build_name: []}
    load_test_files(builds=builds)
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_for_build_with_cyclic_dependence(load_test_files):
    build_name = "test_build"
    builds = {build_name: ["task1"]}
    tasks = {"task1": ["task2"], "task2": ["task1"]}
    load_test_files(builds=builds, tasks=tasks)
    response = client.post("/builds/tasks", json={"name": build_name})
    assert response.status_code == 422
