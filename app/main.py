from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .builds.file_manager import BuildsFileManager
from .builds.router import router as builds_router
from .builds.service import load_files
from .builds.exceptions import TasksCyclicDependence, UnknownBuildName, UnknownTaskName

file_manager = BuildsFileManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_files(file_manager)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(TasksCyclicDependence)
async def tasks_cyclic_dependence_exception_handler(
    request: Request, exc: TasksCyclicDependence
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Unable to sort tasks, cyclic dependency detected."},
    )


@app.exception_handler(UnknownBuildName)
async def unknown_build_name_exception_handler(request: Request, exc: UnknownBuildName):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Incorrect or nonexistent build name."},
    )


@app.exception_handler(UnknownTaskName)
async def unknown_task_name_exception_handler(request: Request, exc: UnknownTaskName):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Build depends on the incorrect or nonexistent task."},
    )


app.include_router(builds_router)
