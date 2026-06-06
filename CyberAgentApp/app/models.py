from pydantic import BaseModel
from typing import Optional

class LoginEvent(BaseModel):
    username: str
    ip_address: str
    location: str
    device: str
    timestamp: str

class AgentDecision(BaseModel):
    risk_score: int
    reason: str
    action: str
