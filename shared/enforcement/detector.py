"""Forbidden Pattern Detector — scans tasks and responses for violations."""
import re
from typing import List

from .types import EnforcementResult, ExecutionContext, GateResult
from .patterns import FORBIDDEN_PATTERNS


class ForbiddenPatternDetector:
    """Detects forbidden patterns in both user tasks and LLM responses."""

    def scan_task(self, task: str) -> List[str]:
        """Scan the USER'S TASK for patterns that require pre-retrieval."""
        detected = []
        for pattern_name, pattern_def in FORBIDDEN_PATTERNS.items():
            if not pattern_def.get("check_task", False):
                continue
            if not pattern_def["patterns"]:
                continue
            for pat in pattern_def["patterns"]:
                if re.search(pat, task, re.IGNORECASE):
                    detected.append(pattern_name)
                    break
        return detected

    def scan_response(self, context: ExecutionContext) -> EnforcementResult:
        """Scan the LLM RESPONSE for forbidden patterns."""
        result = EnforcementResult(gate_result=GateResult.PASS)
        if not context.llm_response:
            return result
        for pattern_name, pattern_def in FORBIDDEN_PATTERNS.items():
            matches = self._check_pattern(context, pattern_name, pattern_def)
            if matches:
                result.forbidden_patterns.append(pattern_name)
                result.missing_references.extend(pattern_def["mandatory_retrieval"])
        if result.forbidden_patterns:
            result.gate_result = GateResult.BLOCK
        return result

    def _check_pattern(self, context: ExecutionContext, name: str, definition: dict) -> bool:
        if "trigger_domains" in definition:
            if not (definition["trigger_domains"] & context.triggered_domains):
                return False
        if not definition["patterns"]:
            return bool(definition.get("trigger_domains", set()) & context.triggered_domains)
        for pattern in definition["patterns"]:
            if re.search(pattern, context.llm_response, re.IGNORECASE):
                return True
        return False


__all__ = ['ForbiddenPatternDetector']