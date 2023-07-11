from fastapi import Request, status
from fastapi.responses import JSONResponse

from .builds.exceptions import TasksCyclicDependence, UnknownBuildName, UnknownTaskName


async def tasks_cyclic_dependence_exception_handler(
    request: Request, exc: TasksCyclicDependence
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Unable to sort tasks, cyclic dependency detected."},
    )


async def unknown_build_name_exception_handler(request: Request, exc: UnknownBuildName):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Incorrect or nonexistent build name."},
    )


async def unknown_task_name_exception_handler(request: Request, exc: UnknownTaskName):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Build depends on the incorrect or nonexistent task."},
    )
