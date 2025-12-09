# Request/response schemas for the API.
from typing import Dict, Any, List
from pydantic import BaseModel
from app.models.graph import GraphCreateRequest
from app.models.state import ExecutionStep


class GraphCreateResponse(BaseModel):
    graph_id: str


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: str
    graph_id: str
    final_state: Dict[str, Any]
    log: List[ExecutionStep]


class GraphStateResponse(BaseModel):
    run_id: str
    graph_id: str
    initial_state: Dict[str, Any]
    final_state: Dict[str, Any]
    log: List[ExecutionStep]


# Convenience alias so routes can reuse the creation schema
GraphCreateBody = GraphCreateRequest
