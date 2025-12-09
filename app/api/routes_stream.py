from fastapi import APIRouter, WebSocket
from app.engine import GraphEngine
from app.store import db

router = APIRouter(prefix="/graph", tags=["stream"])
engine = GraphEngine()


@router.websocket("/stream/{graph_id}")
async def stream(ws: WebSocket, graph_id: str):
    await ws.accept()
    graph = db.get_graph(graph_id)
    if not graph:
        await ws.send_text("Graph not found")
        await ws.close()
        return

    state = {}
    current = graph.start_node
    step = 0

    while current:
        step += 1
        node = graph.get_node(current)
        tool = engine.get_tool(node.tool)
        result = tool(state, node.config) or {}
        await ws.send_json({"step": step, "node": current, "output": result})
        current = result.get("next_node") or graph.get_next_node(current)

    await ws.send_text("DONE")
    await ws.close()
