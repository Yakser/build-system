from collections import defaultdict
from functools import lru_cache

from .exceptions import TasksCyclicDependence, UnknownBuildName, UnknownTaskName
from .file_manager import FileManager

tasks = {}
builds = {}


def load_files(file_manager: FileManager):
    # fixme
    global tasks, builds
    tasks = file_manager.get_tasks_adjacency_list()
    builds = file_manager.get_builds_adjacency_list()


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
        if now not in tasks:
            raise UnknownTaskName()

        for child in tasks[now]:
            if color[child] == 1:
                raise TasksCyclicDependence()
            if color[child] == 0:
                dfs(child)

        color[now] = 2
        stack.append(now)

    dfs(task_name)

    return stack
