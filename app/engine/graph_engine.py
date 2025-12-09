import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from app.models.graph import Graph
from app.models.state import ExecutionStep
from app.engine.tools import get_tool

logger = logging.getLogger("graph_engine")
logging.basicConfig(level=logging.INFO)


class GraphEngine:
    def __init__(self, max_steps: int = 100):
        self.max_steps = max_steps

    def run(self, graph: Graph, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        state: Dict[str, Any] = dict(initial_state)
        log: List[ExecutionStep] = []

        current = graph.start_node
        visited = defaultdict(int)
        step = 0

        while current is not None and step < self.max_steps:
            step += 1
            visited[current] += 1

            node = graph.get_node(current)
            tool = get_tool(node.tool)

            result = tool(state, node.config) or {}
            next_override: Optional[str] = result.pop("next_node", None)

            state.update(result)

            exec_step = ExecutionStep(
                step=step,
                node=current,
                output=result,
                state=dict(state),
            )
            log.append(exec_step)

            logger.info(
                f"[{step}] node={current}, output={result}, next={next_override or graph.get_next_node(current)}"
            )

            current = next_override if next_override is not None else graph.get_next_node(current)

        return {
            "final_state": state,
            "log": log,
        }
