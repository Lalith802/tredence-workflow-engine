from fastapi import FastAPI
from app.api.routes_graph import router as graph_router
from app.api.routes_stream import router as stream_router
from app.engine.workflows import code_review  # forces tool registration
from app.engine.tools import TOOL_REGISTRY

app = FastAPI(
    title="Tredence Workflow & Streaming Engine",
    version="2.0.0",
    description="Graph execution, branching, looping, DB persistence, and WebSocket streaming."
)

app.include_router(graph_router)
app.include_router(stream_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "registered_tools": list(TOOL_REGISTRY.keys())
    }
