import abc
import os

import yaml

from app.builds.typings import AdjacencyList
from app.constants import STATIC_DIR


class FileManager(abc.ABC):
    @abc.abstractmethod
    def get_tasks_adjacency_list(self) -> AdjacencyList:
        pass

    @abc.abstractmethod
    def get_builds_adjacency_list(self) -> AdjacencyList:
        pass

    @staticmethod
    def read_tasks():
        return FileManager._read_yaml("tasks.yaml")["tasks"]

    @staticmethod
    def read_builds():
        return FileManager._read_yaml("builds.yaml")["builds"]

    @staticmethod
    def _read_yaml(filename: str) -> dict:
        file_path = os.path.join(STATIC_DIR, filename)
        with open(file_path) as file:
            return yaml.safe_load(file)


class BuildsFileManager(FileManager):
    def get_tasks_adjacency_list(self) -> AdjacencyList:
        adj_list = {}
        for task in self.read_tasks():
            adj_list[task["name"]] = task["dependencies"]
        return adj_list

    def get_builds_adjacency_list(self) -> AdjacencyList:
        adj_list = {}
        for build in self.read_builds():
            adj_list[build["name"]] = build["tasks"]
        return adj_list


class MockBuildsFileManager(FileManager):
    def __init__(
        self,
        tasks_adj_list: AdjacencyList | None = None,
        builds_adj_list: AdjacencyList | None = None,
    ):
        self.tasks = tasks_adj_list
        if self.tasks is None:
            self.tasks = {
                "test_task1": ["test_task2", "test_task3"],
                "test_task2": [],
                "test_task3": [],
                "test_task4": ["test_task5"],
                "test_task5": [],
                "test_task6": [],
            }
        self.builds = builds_adj_list
        if self.builds is None:
            self.builds = {
                "test_build": [
                    "test_task1",
                    "test_task4",
                    "test_task6",
                ]
            }

    def get_tasks_adjacency_list(self) -> AdjacencyList:
        return self.tasks

    def get_builds_adjacency_list(self) -> AdjacencyList:
        return self.builds
