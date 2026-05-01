"""Enforcement Engine — fail-closed governance with recursion guard."""
from pathlib import Path
from typing import Callable, List
from datetime import datetime, timezone

from .types import (
    EnforcementResult, ExecutionContext, GateResult,
    ConfidenceLevel, MAX_ENFORCEMENT_ATTEMPTS,
)
from .audit import AuditTrail
from .gates import PreExecutionGate, PostExecutionGate


class EnforcementEngine:
    """Fail-closed enforcement engine with recursion guard and audit trail."""

    def __init__(self, reference_dir: Path):
        self.reference_dir = Path(reference_dir)
        self.pre_gate = PreExecutionGate(self.reference_dir)
        self.post_gate = PostExecutionGate(self.reference_dir)
        self.audit = AuditTrail(self.reference_dir)
        self.max_attempts = MAX_ENFORCEMENT_ATTEMPTS

    def load_reference(self, ref_path: Path):
        from .types import LoadedReference
        import hashlib
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference not found: {ref_path}")
        content = ref_path.read_text(encoding='utf-8')
        return LoadedReference(
            path=ref_path, content=content,
            size_bytes=len(content.encode('utf-8')),
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            loaded_at=datetime.now(timezone.utc)
        )

    def force_load_references(self, context: ExecutionContext, ref_names: List[str]):
        for ref_name in ref_names:
            full_path = self.reference_dir / ref_name
            if full_path.exists():
                already_loaded = any(r.path == full_path for r in context.loaded_references)
                if not already_loaded:
                    loaded = self.load_reference(full_path)
                    context.loaded_references.append(loaded)
                    context.retrieved_reference_paths.append(full_path)

    def execute_with_enforcement(
        self,
        context: ExecutionContext,
        llm_call_fn: Callable[[ExecutionContext], str],
        attempt: int = 1
    ) -> EnforcementResult:
        context.enforcement_attempts = attempt
        if attempt > self.max_attempts:
            self.audit.append("FATAL_MAX_ATTEMPTS", {
                "task": context.task[:500], "attempts": attempt,
                "triggered_domains": list(context.triggered_domains),
            })
            return EnforcementResult(
                gate_result=GateResult.FATAL, attempt_number=attempt,
                violations=[f"Max attempts ({self.max_attempts}) exceeded. Human intervention required."],
                escalation_reason="Repeated governance failure", escalation_domain="SYSTEM"
            )
        self.audit.append("PRE_GATE_START", {"task": context.task[:500], "attempt": attempt, "domains": list(context.triggered_domains)})
        pre_result = self.pre_gate.validate(context)
        if pre_result.gate_result == GateResult.BLOCK:
            self.audit.append("PRE_GATE_BLOCK", {"violations": pre_result.violations, "missing_refs": pre_result.missing_references, "attempt": attempt})
            self.force_load_references(context, pre_result.missing_references)
            return self.execute_with_enforcement(context, llm_call_fn, attempt + 1)
        self.audit.append("LLM_EXECUTION_START", {"attempt": attempt, "loaded_ref_count": len(context.loaded_references)})
        try:
            context.llm_response = llm_call_fn(context)
        except Exception as e:
            self.audit.append("LLM_EXECUTION_FAILURE", {"error": str(e), "attempt": attempt})
            return EnforcementResult(gate_result=GateResult.BLOCK, attempt_number=attempt, violations=[f"LLM execution failed: {str(e)}"])
        self.audit.append("POST_GATE_START", {"attempt": attempt, "response_length": len(context.llm_response) if context.llm_response else 0})
        post_result = self.post_gate.validate(context)
        post_result.attempt_number = attempt
        if post_result.gate_result == GateResult.BLOCK:
            self.audit.append("POST_GATE_BLOCK", {"violations": post_result.violations, "forbidden_patterns": post_result.forbidden_patterns, "missing_refs": post_result.missing_references, "attempt": attempt})
            self.force_load_references(context, post_result.missing_references)
            return self.execute_with_enforcement(context, llm_call_fn, attempt + 1)
        if post_result.gate_result == GateResult.ESCALATE:
            self.audit.append("ESCALATION", {"domain": post_result.escalation_domain, "reason": post_result.escalation_reason, "confidence": post_result.confidence.value})
            context.llm_response = f"ESCALATION REQUIRED - Domain: {post_result.escalation_domain} - Reason: {post_result.escalation_reason} - Risk: Not validated against production incidents - Action: Human review before implementation --- {context.llm_response}"
        if post_result.confidence == ConfidenceLevel.UNTESTED:
            context.llm_response = f"CONFIDENCE: UNTESTED - Not validated against production incidents - Consider testing in isolation - --- {context.llm_response}"
        self.audit.append("EXECUTION_COMPLETE", {"attempt": attempt, "gate": post_result.gate_result.value, "confidence": post_result.confidence.value})
        return post_result


class OutcomeLogger:
    """Decision feedback loop integration."""

    def __init__(self, reference_dir: Path):
        self.reference_dir = Path(reference_dir)
        self.audit = AuditTrail(reference_dir)

    def record_outcome(self, context: ExecutionContext, result: EnforcementResult, actual_outcome: str = None):
        self.audit.append("DECISION_OUTCOME", {
            "task": context.task[:500], "domains": list(context.triggered_domains),
            "confidence": result.confidence.value, "gate_result": result.gate_result.value,
            "attempts": result.attempt_number, "violations": result.violations,
            "actual_outcome": actual_outcome or "Not yet recorded",
        })

    def record_failure(self, context: ExecutionContext, result: EnforcementResult, failure_description: str):
        self.audit.append("FAILURE_POSTMORTEM", {
            "task": context.task[:500], "failure": failure_description,
            "domains": list(context.triggered_domains),
            "confidence": result.confidence.value, "gate_result": result.gate_result.value,
            "violations": result.violations, "forbidden_patterns": result.forbidden_patterns,
        })


__all__ = ['EnforcementEngine', 'OutcomeLogger']