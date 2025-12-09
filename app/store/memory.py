# In-memory storage for graphs and runs (or DB wiring later).
from typing import Dict, Optional
import uuid
from app.models.graph import Graph
from app.models.state import RunRecord

_GRAPHS: Dict[str, Graph] = {}
_RUNS: Dict[str, RunRecord] = {}


def save_graph(graph: Graph) -> str:
    _GRAPHS[graph.graph_id] = graph
    return graph.graph_id


def get_graph(graph_id: str) -> Optional[Graph]:
    return _GRAPHS.get(graph_id)


def new_run_id() -> str:
    return str(uuid.uuid4())


def save_run(run: RunRecord) -> str:
    _RUNS[run.run_id] = run
    return run.run_id


def get_run(run_id: str) -> Optional[RunRecord]:
    return _RUNS.get(run_id)
