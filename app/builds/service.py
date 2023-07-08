import os
from collections import defaultdict
from functools import lru_cache

import yaml

from .exceptions import UnknownBuildName, TasksCyclicDependence
from ..constants import STATIC_DIR

tasks = {}
builds = {}


def load_files():
    # fixme
    global tasks, builds
    tasks = get_tasks_adjacency_list()
    builds = get_builds_adjacency_list()


def get_tasks_adjacency_list() -> dict[str, list[str]]:
    adj_list = {}
    for task in read_tasks():
        adj_list[task["name"]] = task["dependencies"]
    return adj_list


def get_builds_adjacency_list() -> dict[str, list[str]]:
    adj_list = {}
    for build in read_builds():
        adj_list[build["name"]] = build["tasks"]
    return adj_list


def read_tasks():
    return read_yaml("tasks.yaml")["tasks"]


def read_builds():
    return read_yaml("builds.yaml")["builds"]


def read_yaml(filename: str) -> dict:
    file_path = os.path.join(STATIC_DIR, filename)
    with open(file_path) as file:
        return yaml.safe_load(file)


@lru_cache
def get_tasks_for_build(name: str) -> list[str]:
    if name not in builds:
        raise UnknownBuildName()

    sorted_tasks = []
    for task in builds[name]:
        sorted_tasks.extend(topological_sort(task))
    return sorted_tasks


@lru_cache
def topological_sort(task_name: str) -> list[str]:
    stack = []
    color = defaultdict(int)

    def dfs(now):
        if color[now] == 1:
            raise TasksCyclicDependence()

        color[now] = 1
        for child in tasks[now]:
            if color[child] == 1:
                raise TasksCyclicDependence()
            if color[child] == 0:
                dfs(child)

        color[now] = 2
        stack.append(now)

    dfs(task_name)

    return stack
