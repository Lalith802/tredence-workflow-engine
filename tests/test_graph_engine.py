# Basic tests for the workflow engine.
from app.engine import GraphEngine  # ensures tools & workflows loaded
from app.models.graph import GraphCreateRequest, NodeModel, EdgeModel, Graph


def test_simple_run():
    req = GraphCreateRequest(
        nodes=[
            NodeModel(name="extract", tool="extract_functions"),
            NodeModel(name="complexity", tool="check_complexity"),
            NodeModel(name="detect_issues", tool="detect_basic_issues"),
            NodeModel(
                name="suggest",
                tool="suggest_improvements",
                config={"threshold": 3.0},
            ),
        ],
        edges=[
            EdgeModel(source="extract", target="complexity"),
            EdgeModel(source="complexity", target="detect_issues"),
            EdgeModel(source="detect_issues", target="suggest"),
        ],
        start_node="extract",
    )

    graph = Graph.from_create_request(req)
    engine = GraphEngine()

    initial_state = {
        "code": "def foo():\n    pass\n",
    }

    result = engine.run(graph, initial_state)
    final_state = result["final_state"]

    assert "quality_score" in final_state
    assert "suggestions" in final_state
