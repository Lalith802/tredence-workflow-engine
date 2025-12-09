from fastapi import APIRouter, HTTPException
from app.api.schemas import (
    GraphCreateBody,
    GraphRunRequest,
    GraphRunResponse,
    GraphStateResponse
)
from app.models.graph import Graph
from app.engine import GraphEngine
from app.store import db
from app.models.state import RunRecord

router = APIRouter(prefix="/graph", tags=["workflow"])
engine = GraphEngine()


@router.post("/create")
def create_graph(body: GraphCreateBody):
    graph = Graph.from_create_request(body)
    graph_id = db.save_graph(graph)
    return {"graph_id": graph_id}


@router.post("/run", response_model=GraphRunResponse)
def run_graph(body: GraphRunRequest):
    graph = db.get_graph(body.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")

    result = engine.run(graph, body.initial_state)

    run = RunRecord(
        run_id=db.new_id(),
        graph_id=graph.graph_id,
        initial_state=body.initial_state,
        final_state=result["final_state"],
        log=result["log"]
    )

    db.save_run(run)

    return GraphRunResponse(
        run_id=run.run_id,
        graph_id=run.graph_id,
        final_state=run.final_state,
        log=run.log
    )


@router.get("/state/{run_id}", response_model=GraphStateResponse)
def get_state(run_id: str):
    run = db.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
