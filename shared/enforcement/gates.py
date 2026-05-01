"""Pre and Post Execution Gates — validate before and after LLM calls."""
from pathlib import Path
from typing import List

from .types import EnforcementResult, ExecutionContext, GateResult, ConfidenceLevel
from .detector import ForbiddenPatternDetector

MANDATORY_REFERENCES = [
    "OPERATING_RULES.md",
    "REFERENCE_RANKING.md",
    "SYSTEM_OVERVIEW.md",
]

DOMAIN_SAFETY_RULES = {
    "financial": ["constraints/regulatory_constraints/"],
    "money": ["constraints/regulatory_constraints/"],
    "payment": ["constraints/regulatory_constraints/"],
    "banking": ["constraints/regulatory_constraints/"],
    "transaction": ["constraints/regulatory_constraints/"],
    "security": ["cybersecurity/", "truth_sources/security_breaches/"],
    "auth": ["cybersecurity/"],
    "authentication": ["cybersecurity/"],
    "encryption": ["cybersecurity/"],
    "vulnerability": ["cybersecurity/", "truth_sources/security_breaches/"],
    "architecture": ["architecture/distributed_systems/", "architecture/system_design/"],
    "scale": ["constraints/high_scale/"],
    "scaling": ["constraints/high_scale/", "truth_sources/scaling_failures/"],
    "throughput": ["constraints/high_scale/"],
    "concurrent": ["constraints/high_scale/"],
    "distributed": ["architecture/distributed_systems/", "failure_modes/distributed_system_traps/"],
    "refactor": ["engineering_decisions/kill_decisions/", "engineering_decisions/tradeoff_analysis/"],
    "rewrite": ["engineering_decisions/kill_decisions/", "truth_sources/why_systems_died/"],
    "rebuild": ["engineering_decisions/kill_decisions/", "truth_sources/why_systems_died/"],
}


class PreExecutionGate:
    """Validates context before LLM execution."""

    def __init__(self, reference_dir: Path):
        self.reference_dir = reference_dir
        self.pattern_detector = ForbiddenPatternDetector()

    def validate(self, context: ExecutionContext) -> EnforcementResult:
        result = EnforcementResult(gate_result=GateResult.PASS)
        missing_mandatory = self._check_mandatory_loaded(context)
        if missing_mandatory:
            result.missing_references.extend(missing_mandatory)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"Mandatory references not loaded: {missing_mandatory}")
        task_patterns = self.pattern_detector.scan_task(context.task)
        if task_patterns:
            for pattern_name in task_patterns:
                pattern_def = FORBIDDEN_PATTERNS[pattern_name]
                result.missing_references.extend(pattern_def["mandatory_retrieval"])
                result.violations.append(f"Task contains pattern '{pattern_name}': {pattern_def['why_blocked']}")
        missing_loaded = self._check_references_actually_loaded(context)
        if missing_loaded:
            result.missing_references.extend(missing_loaded)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"References not loaded: {missing_loaded}")
        domain_missing = self._check_domain_safety(context)
        if domain_missing:
            result.missing_references.extend(domain_missing)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"Domain safety references not loaded: {domain_missing}")
        return result

    def _check_mandatory_loaded(self, context: ExecutionContext) -> List[str]:
        missing = []
        loaded_paths = {str(r.path.name) for r in context.loaded_references}
        for ref in MANDATORY_REFERENCES:
            if ref not in loaded_paths:
                full_path = self.reference_dir / ref
                if full_path.exists():
                    missing.append(f"{ref} (exists but NOT loaded)")
                else:
                    missing.append(f"{ref} (MISSING from disk)")
        return missing

    def _check_references_actually_loaded(self, context: ExecutionContext) -> List[str]:
        missing = []
        for ref_path in context.retrieved_reference_paths:
            loaded = any(r.path == ref_path and r.content.strip() for r in context.loaded_references)
            if not loaded:
                missing.append(str(ref_path))
        return missing

    def _check_domain_safety(self, context: ExecutionContext) -> List[str]:
        missing = []
        loaded_paths = {str(r.path) for r in context.loaded_references}
        for domain in context.triggered_domains:
            if domain in DOMAIN_SAFETY_RULES:
                for required_ref in DOMAIN_SAFETY_RULES[domain]:
                    found = any(required_ref in str(p) for p in loaded_paths)
                    if not found:
                        missing.append(required_ref)
        return missing


class PostExecutionGate:
    """Validates LLM response after execution."""

    def __init__(self, reference_dir: Path):
        self.reference_dir = reference_dir
        self.pattern_detector = ForbiddenPatternDetector()

    def validate(self, context: ExecutionContext) -> EnforcementResult:
        result = EnforcementResult(gate_result=GateResult.PASS)
        forbidden_result = self.pattern_detector.scan_response(context)
        if forbidden_result.gate_result == GateResult.BLOCK:
            result.gate_result = GateResult.BLOCK
            result.forbidden_patterns = forbidden_result.forbidden_patterns
            result.missing_references = forbidden_result.missing_references
            result.violations.append(f"Forbidden patterns in response: {forbidden_result.forbidden_patterns}")
            return result
        result.confidence = self._classify_confidence(context)
        if self._should_escalate(context, result.confidence):
            result.gate_result = GateResult.ESCALATE
            result.escalation_reason = "UNTESTED recommendation in critical domain"
            result.escalation_domain = self._determine_escalation_domain(context)
        return result

    def _classify_confidence(self, context: ExecutionContext) -> ConfidenceLevel:
        loaded_paths = {str(r.path) for r in context.loaded_references}
        has_truth = any("truth_sources" in p for p in loaded_paths)
        has_constraints = any("constraints" in p for p in loaded_paths)
        has_failures = any("failure_modes" in p for p in loaded_paths)
        has_decisions = any("engineering_decisions" in p for p in loaded_paths)
        if has_truth and has_constraints:
            return ConfidenceLevel.VALIDATED
        elif has_failures or has_decisions:
            return ConfidenceLevel.REASONED
        else:
            return ConfidenceLevel.UNTESTED

    def _should_escalate(self, context: ExecutionContext, confidence: ConfidenceLevel) -> bool:
        if confidence != ConfidenceLevel.UNTESTED:
            return False
        critical = {"financial", "security", "architecture", "money", "payment", "banking", "auth", "encryption", "vulnerability", "scale"}
        return bool(context.triggered_domains & critical)

    def _determine_escalation_domain(self, context: ExecutionContext) -> str:
        domain_map = {"financial": "FINANCIAL", "money": "FINANCIAL", "payment": "FINANCIAL", "banking": "FINANCIAL", "transaction": "FINANCIAL", "security": "SECURITY", "auth": "SECURITY", "encryption": "SECURITY", "vulnerability": "SECURITY", "architecture": "ARCHITECTURE", "scale": "ARCHITECTURE"}
        for domain in sorted(context.triggered_domains):
            if domain in domain_map:
                return domain_map[domain]
        return "UNKNOWN"


# Import here to avoid circular dependency
from .patterns import FORBIDDEN_PATTERNS

__all__ = ['PreExecutionGate', 'PostExecutionGate', 'MANDATORY_REFERENCES', 'DOMAIN_SAFETY_RULES']