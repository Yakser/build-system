from fastapi import APIRouter

from .models import BuildModel
from .service import get_tasks_for_build

router = APIRouter(
    prefix="/builds",
    tags=["builds"],
    responses={
        400: {
            "description": "Unknown build name.",
        },
        422: {
            "description": "Build depends on the incorrect or nonexistent task.",
        },
    },
)


@router.post("/tasks", description="Returns sorted list of tasks for given build")
async def tasks_for_build(build: BuildModel) -> list[str]:
    # I think it would be nice to add caching
    return get_tasks_for_build(build.name)
