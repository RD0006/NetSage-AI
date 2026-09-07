from pydantic import BaseModel, Field
from typing import List, Optional


class Device(BaseModel):
    name: str
    ip: Optional[str] = None


class CommandOutput(BaseModel):
    command: str
    output: str


class AnalyzeRequest(BaseModel):
    symptom: str
    devices: List[Device] = Field(default_factory=list)
    connections: List[dict] = Field(default_factory=list)
    commands: List[CommandOutput] = Field(default_factory=list)
    notes: str = ""


class Diagnosis(BaseModel):
    root_cause: str
    fault_domain: str
    osi_layer: str
    confidence: str
    severity: str
    evidence: List[str] = Field(default_factory=list)
    next_command: List[str] = Field(default_factory=list)
    fix_steps: List[str] = Field(default_factory=list)


class CheckerResult(BaseModel):
    issues: List[dict] = Field(default_factory=list)
    issue_count: int