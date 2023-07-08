from fastapi import APIRouter

from .models import BuildModel
from .service import get_tasks_for_build

router = APIRouter(
    prefix="/builds",
    tags=["builds"],
    responses={
        400: {"description": "Unknown build name", }
    },
)


@router.post("/tasks")
async def tasks_for_build(build: BuildModel) -> list[str]:
    return get_tasks_for_build(build.name)
