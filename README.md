# Tredence Workflow Engine

A FastAPI-based backend workflow execution system that runs code-review analysis as a directed graph of tools with shared state, scoring, persistence, and iterative improvement cycles until quality thresholds are achieved. This implementation fulfills and extends the Tredence backend assessment requirements by incorporating looping logic, state propagation, node-to-node execution control, and persistent run storage for full reproducibility.

## Features

- Directed graph execution with clearly defined node transitions
- Shared mutable state maintained and updated across each node run
- Quality scoring that increases as tools evaluate and refine the code
- Loop continuation until the defined quality threshold is met
- Dynamic branching determined by tool output (`next_node`)
- Tool registration using lightweight decorator-based mechanism
- Persistent storage of workflow runs and their final outputs
- Modular separation of tools, engine, models, and routes for scalability

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Storage:** SQLite (persistent run state)
- **Execution Model:** Directed graph with state propagation
- **Environment:** Standard Python runtime, no external ML dependencies

## 📂 Project Structure
```
Tredence/
├── app/
│ ├── main.py # FastAPI application entry point
│ ├── api/
│ │ └── routes_graph.py # Create, run, and fetch workflow runs
│ ├── engine/
│ │ ├── graph_engine.py # Core graph execution logic
│ │ ├── tools.py # Tool registry decorator + lookup
│ │ └── workflows/
│ │ └── code_review.py # Code review tool implementations
│ ├── models/
│ │ ├── graph.py # Node, Edge, and Graph schemas
│ │ └── state.py # Run tracking and state schemas
│ └── store/
│ └── db.py # SQLite persistence layer
├── requirements.txt
├── Dockerfile
└── README.md
```
## API Endpoints

- **GET /health**  
  Returns service status and list of registered tools.

- **POST /graph/create**  
  Defines nodes and edges for the workflow execution structure.

- **POST /graph/run**  
  Executes the created workflow with provided initial state and returns final scoring, detected issues, and improvement results.

- **GET /graph/state/{run_id}**  
  Retrieves stored execution results for any completed workflow using its run identifier.

## Setup

- Install dependencies:
pip install -r requirements.txt

- Start the server:
uvicorn app.main:app --reload

- Open API documentation:
http://127.0.0.1:8000/docs

## Example Graph Definition

**Request**
POST /graph/create

```json
{
  "nodes": [
    { "name": "extract", "tool": "extract_functions" },
    { "name": "complexity", "tool": "check_complexity" },
    { "name": "detect_issues", "tool": "detect_basic_issues" },
    {
      "name": "suggest",
      "tool": "suggest_improvements",
      "config": { "threshold": 6 }
    }
  ],
  "edges": [
    { "source": "extract", "target": "complexity" },
    { "source": "complexity", "target": "detect_issues" },
    { "source": "detect_issues", "target": "suggest" }
  ]
}
```
## Example Run Execution

**Request**
POST /graph/run

```json
{
  "graph_id": "your_graph_id_here",
  "initial_state": {
    "code": "def foo():\n    pass\n\n# TODO fix this\nfor i in range(5): print(i)"
  }
}
``` 
## Sample Response
```json
{
  "run_id": "c3ca5530-5767-4ac2-ba26-e41cc797577b",
  "final_state": {
    "quality_score": 7.7,
    "issue_count": 1,
    "suggestions": ["Fix style & TODO issues."]
  }
}
```
## 📌 Example Execution Output

POST /graph/run


**Body**
```json
{
  "graph_id": "63de51ad-d0d7-45cd-bbc7-926d708595e8",
  "initial_state": {
    "code": "def foo():\n    pass\n\n# TODO fix this\nfor i in range(5): print(i)"
  }
}
```
## Output
```json
{
  "run_id": "c3ca5530-5767-4ac2-ba26-e41cc797577b",
  "graph_id": "63de51ad-d0d7-45cd-bbc7-926d708595e8",
  "final_state": {
    "code": "def foo():\n    pass\n\n# TODO fix this\nfor i in range(5): print(i)",
    "quality_score": 7.7,
    "functions": ["def foo():"],
    "num_functions": 1,
    "complexity_score": 6,
    "issues": ["1 TODO comments"],
    "issue_count": 1,
    "suggestions": ["Fix style & TODO issues."]
  }
}
```
## Execution Log (Step-by-Step)
```json
[
  { "step": 1, "node": "extract", "quality_score": 1 },
  { "step": 2, "node": "complexity", "quality_score": 2 },
  { "step": 3, "node": "detect_issues", "quality_score": 2.9 },
  { "step": 4, "node": "suggest", "quality_score": 3.9 },
  { "step": 5, "node": "detect_issues", "quality_score": 4.8 },
  { "step": 6, "node": "suggest", "quality_score": 5.8 },
  { "step": 7, "node": "detect_issues", "quality_score": 6.7 },
  { "step": 8, "node": "suggest", "quality_score": 7.7 }
]
```
## Demo Screenshots
<img width="1178" height="927" alt="image" src="https://github.com/user-attachments/assets/118ac436-ba94-4ce0-9c1c-200896e18d8a" />

<img width="718" height="734" alt="image" src="https://github.com/user-attachments/assets/a889e201-0d16-4d74-9c10-bc95100ff4d9" />

<img width="720" height="863" alt="image" src="https://github.com/user-attachments/assets/68fbb81f-9644-4354-96e9-13bce6e9039d" />

## Conclusion

This project successfully implements a modular workflow execution engine where each analysis stage runs as a node in a directed graph with shared state propagation. The iterative loop mechanism incrementally improves code quality until defined thresholds are met, demonstrating robust and fault-tolerant execution. The system further supports persistent run storage, reproducible evaluations, and clear tooling registry, making it both scalable and extensible for advanced code analysis use cases.

## Author

- **Name:** Lalith Krishna Vallamkonda  
- **Roll Number:** RA2211056010095  
- **Program:** B.Tech CSE (Data Science)  
- **Project:** Tredence Workflow Engine – Code Quality Assessment

---
