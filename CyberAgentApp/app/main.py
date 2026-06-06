from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

# ---------------------------------------------------------
#  FIXED IMPORTS (LOCAL MODULES)
# ---------------------------------------------------------
from agent import CyberAgent
from database import save_event
from actions import block_ip, disable_user, quarantine_host
from ai import explain_event


# ---------------------------------------------------------
#  FASTAPI APP + CORS
# ---------------------------------------------------------
app = FastAPI(title="Cybersecurity Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CyberAgent()


# ---------------------------------------------------------
#  MODELS
# ---------------------------------------------------------
class SecurityEvent(BaseModel):
    source: str
    event_type: str
    payload: Dict[str, Any]


# ---------------------------------------------------------
#  ROUTES
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "cybersecurity agent online"}


@app.post("/ingest_event")
def ingest_event(event: SecurityEvent):
    event_dict = event.dict()
    save_event(event_dict)
    analysis = agent.process_event(event_dict)
    return {"analysis": analysis}


@app.post("/analyze")
def analyze(payload: Dict[str, Any]):
    return {"result": agent.analyze(payload)}


@app.post("/action")
def take_action(payload: Dict[str, Any]):
    action = payload.get("action")
    target = payload.get("target")

    if not action or not target:
        raise HTTPException(status_code=400, detail="Missing 'action' or 'target'")

    actions_map = {
        "block_ip": block_ip,
        "disable_user": disable_user,
        "quarantine_host": quarantine_host,
    }

    if action not in actions_map:
        raise HTTPException(status_code=400, detail=f"Unknown action '{action}'")

    return {"result": actions_map[action](target)}


@app.post("/explain")
def explain(payload: Dict[str, Any]):
    return {"explanation": explain_event(payload)}


# ---------------------------------------------------------
#  CORRELATION ENDPOINT
# ---------------------------------------------------------
@app.post("/correlate")
def correlate(payload: Dict[str, Any]):
    if "events" not in payload:
        return {"incident": {"error": "Missing 'events' field"}}

    events = payload["events"]

    if not isinstance(events, list):
        return {"incident": {"error": "'events' must be a list"}}

    try:
        incident = agent.correlate(events)
    except Exception as e:
        return {"incident": {"error": "Correlation engine crashed", "details": str(e)}}

    return {"incident": incident or {"message": "No correlation detected"}}
