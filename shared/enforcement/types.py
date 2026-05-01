"""Enforcement types — enums and dataclasses for the governance engine."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Set
from pathlib import Path
from datetime import datetime

MAX_ENFORCEMENT_ATTEMPTS = 3
AUDIT_LOG_DIR = "audit_trail"


class ConfidenceLevel(Enum):
    VALIDATED = "validated"
    REASONED = "reasoned"
    UNTESTED = "untested"


class GateResult(Enum):
    PASS = "pass"
    BLOCK = "block"
    ESCALATE = "escalate"
    FATAL = "fatal"


@dataclass
class LoadedReference:
    """Distinguishes existence from actual injection into context."""
    path: Path
    content: str
    size_bytes: int
    content_hash: str
    loaded_at: datetime


@dataclass
class EnforcementResult:
    gate_result: GateResult
    confidence: ConfidenceLevel = ConfidenceLevel.UNTESTED
    missing_references: List[str] = field(default_factory=list)
    forbidden_patterns: List[str] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)
    escalation_reason: Optional[str] = None
    escalation_domain: Optional[str] = None
    attempt_number: int = 1
    loaded_references: List[LoadedReference] = field(default_factory=list)


@dataclass
class ExecutionContext:
    task: str
    triggered_domains: Set[str] = field(default_factory=set)
    retrieved_reference_paths: List[Path] = field(default_factory=list)
    loaded_references: List[LoadedReference] = field(default_factory=list)
    llm_response: Optional[str] = None
    confidence_override: Optional[ConfidenceLevel] = None
    enforcement_attempts: int = 0


__all__ = [
    'ConfidenceLevel', 'GateResult', 'LoadedReference',
    'EnforcementResult', 'ExecutionContext',
    'MAX_ENFORCEMENT_ATTEMPTS', 'AUDIT_LOG_DIR',
]