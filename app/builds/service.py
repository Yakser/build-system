from collections import defaultdict
from enum import Enum

from .exceptions import TasksCyclicDependence, UnknownBuildName, UnknownTaskName
from .file_manager import FileManager

tasks = {}
builds = {}


def load_files(file_manager: FileManager):
    # fixme: maybe should store data in DB and not use global variables
    global tasks, builds
    tasks = file_manager.get_tasks_adjacency_list()
    builds = file_manager.get_builds_adjacency_list()


def get_tasks_for_build(name: str) -> list[str]:
    if name not in builds:
        raise UnknownBuildName()

    sorted_tasks = []
    for task in builds[name]:
        sorted_tasks.extend(topological_sort(task))
    return sorted_tasks


def topological_sort(task_name: str) -> list[str]:
    """
    Returns a sorted list of tasks, first come the dependencies of the task, then the current task.

    The implementation uses the topological sort algorithm (https://www.geeksforgeeks.org/topological-sorting/) and
    DFS (https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)
    """

    class Color(str, Enum):
        WHITE = 0  # means that vertex with this color is not visited
        GRAY = (
            1  # means that vertex with this color is visited and it is in current path
        )
        BLACK = (
            2  # means that vertex with this color is visited and all its children too
        )

    stack = []
    color = defaultdict(lambda: Color.WHITE)

    def dfs(now):
        if color[now] == Color.GRAY:
            raise TasksCyclicDependence()

        color[now] = Color.GRAY
        if now not in tasks:
            raise UnknownTaskName()

        for child in tasks[now]:
            if color[child] == Color.GRAY:
                raise TasksCyclicDependence()
            if color[child] == Color.WHITE:
                dfs(child)

        color[now] = Color.BLACK
        stack.append(now)

    dfs(task_name)

    return stack
