from contextlib import asynccontextmanager

from fastapi import FastAPI

from .builds.exceptions import TasksCyclicDependence, UnknownBuildName, UnknownTaskName
from .builds.file_manager import BuildsFileManager
from .builds.router import router as builds_router
from .builds.service import load_files
from .exception_handlers import (
    tasks_cyclic_dependence_exception_handler,
    unknown_build_name_exception_handler,
    unknown_task_name_exception_handler,
)

file_manager = BuildsFileManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_files(file_manager)
    yield


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(
    TasksCyclicDependence, tasks_cyclic_dependence_exception_handler
)
app.add_exception_handler(UnknownBuildName, unknown_build_name_exception_handler)
app.add_exception_handler(UnknownTaskName, unknown_task_name_exception_handler)

app.include_router(builds_router)
