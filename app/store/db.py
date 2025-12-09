import uuid
import sqlite3
from app.models.graph import Graph
from app.models.state import RunRecord

conn = sqlite3.connect("workflow.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS graphs (id TEXT PRIMARY KEY, graph TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, run TEXT)")


def new_id():
    return str(uuid.uuid4())


def save_graph(graph: Graph):
    cursor.execute("INSERT OR REPLACE INTO graphs VALUES (?, ?)", (graph.graph_id, graph.json()))
    conn.commit()
    return graph.graph_id


def get_graph(graph_id: str):
    row = cursor.execute("SELECT graph FROM graphs WHERE id=?", (graph_id,)).fetchone()
    return Graph.parse_raw(row[0]) if row else None


def save_run(run: RunRecord):
    cursor.execute("INSERT OR REPLACE INTO runs VALUES (?, ?)", (run.run_id, run.json()))
    conn.commit()
    return run.run_id


def get_run(run_id: str):
    row = cursor.execute("SELECT run FROM runs WHERE id=?", (run_id,)).fetchone()
    return RunRecord.parse_raw(row[0]) if row else None
