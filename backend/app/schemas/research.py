from pydantic import BaseModel
from typing import List, Optional


class SourceItem(BaseModel):
    title: str
    url: str
    content: str
    score: float
    domain: str


class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    query: str
    source_count: int
    sources: List[SourceItem]
    analysis: str
    critique: str
    report: str