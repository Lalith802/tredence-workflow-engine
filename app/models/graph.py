# Pydantic models for Graph, Nodes, Edges.
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid


class NodeModel(BaseModel):
    name: str
    tool: str  # name of tool in registry
    config: Dict[str, Any] = Field(default_factory=dict)


class EdgeModel(BaseModel):
    source: str
    target: str


class GraphCreateRequest(BaseModel):
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    start_node: str


class Graph(BaseModel):
    graph_id: str
    nodes: Dict[str, NodeModel]
    edges: List[EdgeModel]
    start_node: str

    @classmethod
    def from_create_request(cls, req: GraphCreateRequest, graph_id: Optional[str] = None) -> "Graph":
        return cls(
            graph_id=graph_id or str(uuid.uuid4()),
            nodes={n.name: n for n in req.nodes},
            edges=req.edges,
            start_node=req.start_node,
        )

    def get_node(self, name: str) -> NodeModel:
        return self.nodes[name]

    def get_next_node(self, current: str) -> Optional[str]:
        for e in self.edges:
            if e.source == current:
                return e.target
        return None
