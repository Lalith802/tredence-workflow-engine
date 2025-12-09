# Pydantic model or dict-like state representation.
from typing import Dict, Any, List
from pydantic import BaseModel


class ExecutionStep(BaseModel):
    step: int
    node: str
    output: Dict[str, Any]
    state: Dict[str, Any]


class RunRecord(BaseModel):
    run_id: str
    graph_id: str
    initial_state: Dict[str, Any]
    final_state: Dict[str, Any]
    log: List[ExecutionStep]
