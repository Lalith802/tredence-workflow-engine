from typing import Dict, Any
from app.engine.tools import register_tool, TOOL_REGISTRY


def _init_quality(state):
    if "quality_score" not in state:
        state["quality_score"] = 0.0


@register_tool("extract_functions")
def extract_functions(state: Dict[str, Any], config: Dict[str, Any]):
    code = state.get("code", "")
    functions = [ln.strip() for ln in code.splitlines() if ln.strip().startswith("def ")]
    _init_quality(state)

    return {
        "functions": functions,
        "num_functions": len(functions),
        "quality_score": state["quality_score"] + 1
    }


@register_tool("check_complexity")
def check_complexity(state: Dict[str, Any], config: Dict[str, Any]):
    code = state.get("code", "")
    lines = [ln for ln in code.splitlines() if ln.strip()]
    loops = sum(1 for ln in lines if "for " in ln or "while " in ln)

    score = len(lines) + (2 * loops)
    _init_quality(state)

    penalty = 2 if score > 50 else 1 if score > 20 else 0

    return {
        "complexity_score": score,
        "quality_score": state["quality_score"] + 1 - penalty
    }


@register_tool("detect_basic_issues")
def detect_basic_issues(state: Dict[str, Any], config: Dict[str, Any]):
    code = state.get("code", "")
    lines = code.splitlines()

    todos = [i for i, ln in enumerate(lines, 1) if "TODO" in ln]
    long_lines = [i for i, ln in enumerate(lines, 1) if len(ln) > 120]

    issues = []
    if todos:
        issues.append(f"{len(todos)} TODO comments")
    if long_lines:
        issues.append(f"{len(long_lines)} long lines")

    _init_quality(state)

    return {
        "issues": issues,
        "issue_count": len(issues),
        "quality_score": max(state["quality_score"] + 1.2 - (0.3 * len(issues)), 0)
    }


@register_tool("suggest_improvements")
def suggest_improvements(state: Dict[str, Any], config: Dict[str, Any]):
    threshold = config.get("threshold", 6)
    quality = state.get("quality_score", 0)
    suggestions = []

    if state.get("complexity_score", 0) > 50:
        suggestions.append("Reduce complexity.")

    if state.get("issue_count", 0) > 0:
        suggestions.append("Fix style & TODO issues.")

    if not suggestions:
        suggestions.append("Add type hints & docstrings.")

    next_node = None if quality >= threshold else "detect_issues"

    return {
        "suggestions": suggestions,
        "quality_score": quality + 1,
        "next_node": next_node
    }


print("Tools registered:", list(TOOL_REGISTRY.keys()))
