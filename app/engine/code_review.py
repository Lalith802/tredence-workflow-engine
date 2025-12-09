"""
Option A: Code Review Mini-Agent

1. extract_functions
2. check_complexity
3. detect_issues
4. suggest_improvements
5. Loop until quality_score >= threshold
"""

from typing import Dict, Any, List
from app.engine.tools import register_tool


def _init_quality(state: Dict[str, Any]) -> None:
    if "quality_score" not in state:
        state["quality_score"] = 0.0


@register_tool("extract_functions")
def extract_functions(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Very simple fake parser:
    - splits code by lines
    - each `def ` line is a function
    """
    code: str = state.get("code", "")
    lines = code.splitlines()
    functions: List[str] = [ln.strip() for ln in lines if ln.strip().startswith("def ")]

    _init_quality(state)
    return {
        "functions": functions,
        "num_functions": len(functions),
        "quality_score": state["quality_score"] + 1.0,
    }


@register_tool("check_complexity")
def check_complexity(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fake complexity metric:
    - count total lines and 'for'/'while' occurrences
    """
    code: str = state.get("code", "")
    lines = [ln for ln in code.splitlines() if ln.strip()]
    loops = sum(1 for ln in lines if "for " in ln or "while " in ln)

    complexity_score = len(lines) + 2 * loops
    _init_quality(state)

    penalty = 0.0
    if complexity_score > 50:
        penalty = 2.0
    elif complexity_score > 20:
        penalty = 1.0

    return {
        "complexity_score": complexity_score,
        "quality_score": state["quality_score"] + 1.0 - penalty,
    }


@register_tool("detect_basic_issues")
def detect_basic_issues(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Very basic rule-based checks:
    - long lines > 120 chars
    - TODO comments
    """
    code: str = state.get("code", "")
    lines = code.splitlines()

    long_lines = [i for i, ln in enumerate(lines, start=1) if len(ln) > 120]
    todos = [i for i, ln in enumerate(lines, start=1) if "TODO" in ln]

    issues: List[str] = []
    if long_lines:
        issues.append(f"{len(long_lines)} long lines (>120 chars)")
    if todos:
        issues.append(f"{len(todos)} TODO comments")

    issue_count = len(issues)
    _init_quality(state)
    score_delta = max(0.0, 1.5 - 0.3 * issue_count)

    return {
        "issues": issues,
        "issue_count": issue_count,
        "quality_score": state["quality_score"] + score_delta,
    }


@register_tool("suggest_improvements")
def suggest_improvements(state: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Suggest simple textual improvements.
    Looping logic: if quality_score < threshold, re-run some nodes.
    """
    threshold: float = config.get("threshold", 5.0)
    quality_score: float = state.get("quality_score", 0.0)

    suggestions: List[str] = []

    if state.get("complexity_score", 0) > 50:
        suggestions.append("Break large functions into smaller ones.")
    if state.get("issue_count", 0) > 0:
        suggestions.append("Fix the reported style / TODO issues.")
    if not suggestions:
        suggestions.append("Code looks reasonable. Consider adding type hints and docstrings.")

    # Decide next node for loop
    if quality_score >= threshold:
        next_node = None  # stop
    else:
        # loop back to detect_basic_issues for one more refinement cycle
        next_node = "detect_issues"

    return {
        "suggestions": suggestions,
        "quality_score": quality_score + 1.0,
        "next_node": next_node,
    }
