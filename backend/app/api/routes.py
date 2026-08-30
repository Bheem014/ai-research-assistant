from fastapi import APIRouter, HTTPException
from app.schemas.research import ResearchRequest, ResearchResponse
from app.orchestrator.research_orchestrator import ResearchOrchestrator

router = APIRouter()
orchestrator = ResearchOrchestrator()


@router.post("/research", response_model=ResearchResponse)
async def conduct_research(payload: ResearchRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = await orchestrator.research(query=payload.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research pipeline error: {str(e)}")