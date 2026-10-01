from fastapi import APIRouter
from pydantic import BaseModel

from app.orchestrator.research_orchestrator import (
    ResearchOrchestrator,
)


router = APIRouter(
    prefix="/api/research",
    tags=["Research"],
)


class ResearchRequest(BaseModel):
    query: str


orchestrator = ResearchOrchestrator()


@router.post("/")
async def start_research(
    request: ResearchRequest,
):
    result = await orchestrator.research(
        request.query
    )

    return {
        "status": "success",
        "data": result,
    }