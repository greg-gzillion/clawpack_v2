# claw_coder/engine/enforcement.py
# VERSION 2.0 - Production Hardened

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Set, Callable, Tuple
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone


# =============================================================================
# CONSTANTS
# =============================================================================

MAX_ENFORCEMENT_ATTEMPTS = 3
AUDIT_LOG_DIR = "audit_trail"


# =============================================================================
# TYPES
# =============================================================================

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


# =============================================================================
# IMMUTABLE AUDIT TRAIL
# =============================================================================

class AuditTrail:
    """Append-only, hash-chained audit log. Immutable by design."""
    
    def __init__(self, base_dir: Path):
        self.audit_dir = base_dir / AUDIT_LOG_DIR
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self._chain_file = self.audit_dir / "CHAIN.json"
        self._ensure_chain()
    
    def _ensure_chain(self):
        if not self._chain_file.exists():
            self._chain_file.write_text(json.dumps({
                "genesis": hashlib.sha256(b"CLAWPACK_AUDIT_GENESIS").hexdigest(),
                "entries": []
            }, indent=2))
    
    def _read_chain(self) -> dict:
        return json.loads(self._chain_file.read_text())
    
    def _write_chain(self, chain: dict):
        self._chain_file.write_text(json.dumps(chain, indent=2))
    
    def append(self, event_type: str, data: dict) -> str:
        """Append immutable entry to audit chain. Returns entry hash."""
        chain = self._read_chain()
        
        previous_hash = chain["entries"][-1]["hash"] if chain["entries"] else chain["genesis"]
        
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "previous_hash": previous_hash,
            "data": data,
        }
        
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()
        
        chain["entries"].append(entry)
        self._write_chain(chain)
        
        # Also write human-readable log
        log_file = self.audit_dir / f"event_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        log_file.write_text(json.dumps(entry, indent=2))
        
        return entry["hash"]
    
    def verify_integrity(self) -> bool:
        """Verify entire chain has not been tampered with."""
        chain = self._read_chain()
        expected = chain["genesis"]
        
        for entry in chain["entries"]:
            if entry["previous_hash"] != expected:
                return False
            
            recalc = hashlib.sha256(
                json.dumps({
                    k: v for k, v in entry.items() 
                    if k != "hash"
                }, sort_keys=True).encode()
            ).hexdigest()
            
            if recalc != entry["hash"]:
                return False
            
            expected = entry["hash"]
        
        return True


# =============================================================================
# FORBIDDEN PATTERN DETECTOR (Now scans both TASK and RESPONSE)
# =============================================================================

FORBIDDEN_PATTERNS = {
    "premature_optimization": {
        "patterns": [
            r"optimize\s+(this|it)\s+early",
            r"we\s+should\s+optimize\s+(this|now)",
            r"let'?s?\s+optimize\s+before",
            r"premature\s+optimization\s+is",
        ],
        "why_blocked": "Premature optimization killed countless projects",
        "mandatory_retrieval": ["failure_modes/premature_optimization/"],
        "check_task": False,
    },
    "rewrite_from_scratch": {
        "patterns": [
            r"rewrite\s+(from\s+scratch|everything|the\s+whole)",
            r"let'?s?\s+rewrite\s+(it|this|the)",
            r"start\s+(over|fresh|from\s+scratch)\s+and\s+rewrite",
            r"burn\s+it\s+down\s+and\s+(rebuild|rewrite)",
            r"rebuild\s+(everything|the\s+whole|from\s+scratch)",
        ],
        "why_blocked": "Rewrites have >70% failure rate",
        "mandatory_retrieval": [
            "engineering_decisions/kill_decisions/",
            "truth_sources/why_systems_died/",
        ],
        "check_task": True,  # Also scan user's task
    },
    "microservices_silver_bullet": {
        "patterns": [
            r"microservices\s+will\s+(solve|fix)\s+this",
            r"just\s+break\s+(it|this)\s+into\s+microservices",
            r"microservices\s+is\s+the\s+answer",
            r"let'?s?\s+microservicize",
        ],
        "why_blocked": "Distributed monolith risk without architecture review",
        "mandatory_retrieval": [
            "architecture/distributed_systems/",
            "failure_modes/distributed_system_traps/",
        ],
        "check_task": False,
    },
    "deferred_safety": {
        "patterns": [
            r"we'?ll\s+add\s+that\s+later",
            r"(security|auth|encryption|compliance).*later",
            r"not\s+(needed|important|critical)\s+(yet|now|for\s+mvp)",
            r"skip\s+(security|auth|validation|compliance)\s+for\s+now",
            r"(compliance|regulatory|security)\s+can\s+wait",
        ],
        "why_blocked": "Deferred safety = no safety. It never gets added.",
        "mandatory_retrieval": [
            "constraints/regulatory_constraints/",
            "truth_sources/security_breaches/",
        ],
        "check_task": False,
    },
    "works_on_my_machine": {
        "patterns": [
            r"works?\s+on\s+my\s+machine",
            r"works?\s+fine?\s+(locally|here|for\s+me)",
        ],
        "why_blocked": "Production reality ignored",
        "mandatory_retrieval": ["truth_sources/production_incidents/"],
        "check_task": False,
    },
    "trendy_thing": {
        "patterns": [
            r"just\s+use\s+(the\s+new|latest|newest)",
            r"everyone\s+is\s+using\s+\w+\s+now",
            r"(switch|migrate)\s+to\s+\w+\s+because\s+(it'?s?\s+new|trending)",
        ],
        "why_blocked": "No production validation for trendy technology",
        "mandatory_retrieval": ["truth_sources/"],
        "check_task": False,
    },
    "framework_magic": {
        "patterns": [
            r"the\s+framework\s+(handles|takes\s+care\s+of|does)\s+that",
            r"(rails|django|spring|react|next\.js)\s+(handles|manages)\s+that",
            r"you\s+don'?t\s+need\s+to\s+worry\s+about\s+that.*framework",
        ],
        "why_blocked": "Abstraction without understanding kills systems",
        "mandatory_retrieval": ["failure_modes/abstraction_leaks/"],
        "check_task": False,
    },
    "no_tests": {
        "patterns": [
            r"(don'?t|doesn'?t|won'?t)\s+need\s+tests?\s+for\s+this",
            r"(skip|skip\s+the|no\s+need\s+for)\s+tests?",
            r"this\s+(is|seems)\s+too\s+simple\s+to\s+test",
        ],
        "why_blocked": "Testing is not optional. No exceptions.",
        "mandatory_retrieval": ["key_guidelines/testing_guidelines/"],
        "check_task": False,
    },
    "financial_no_regulatory": {
        "patterns": [],
        "why_blocked": "Financial system without regulatory review is illegal",
        "mandatory_retrieval": ["constraints/regulatory_constraints/"],
        "check_task": False,
        "trigger_domains": {"financial", "money", "payment", "banking", "transaction"}
    },
    "security_no_cyber": {
        "patterns": [],
        "why_blocked": "Security recommendation without cyber review is reckless",
        "mandatory_retrieval": ["cybersecurity/", "truth_sources/security_breaches/"],
        "check_task": False,
        "trigger_domains": {"security", "auth", "authentication", "encryption", "vulnerability"}
    }
    # =========================================================================
    # LLM SOVEREIGNTY PATTERNS — Constitutional Law
    # =========================================================================
    "direct_ollama_import": {
        "patterns": [
            r"import\s+ollama",
            r"from\s+ollama\s+import",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. "
                       "All model access must route through shared/llm/client.py — the sovereign gateway.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_groq_import": {
        "patterns": [
            r"from\s+groq\s+import",
            r"import\s+groq",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. "
                       "All model access must route through shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_openrouter_call": {
        "patterns": [
            r"openrouter\.ai",
            r"openrouter\.ai/api/v\d/chat/completions",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct OpenRouter API calls bypass the sovereign gateway. "
                       "Use shared/llm/client.py — the single point of model access.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_groq_api_call": {
        "patterns": [
            r"api\.groq\.com",
            r"api\.groq\.com/openai/v\d/chat/completions",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct Groq API calls bypass the sovereign gateway. "
                       "Use shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_ollama_http": {
        "patterns": [
            r"localhost:11434",
            r"localhost:11434/api/generate",
            r"http://localhost:11434",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct Ollama HTTP calls bypass the sovereign gateway. "
                       "Use shared/llm/client.py — the single point of model access.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_anthropic_import": {
        "patterns": [
            r"import\s+anthropic",
            r"from\s+anthropic\s+import",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. "
                       "All model access must route through shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_provider_request": {
        "patterns": [
            r"requests\.post\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
            r"urllib\.request\.urlopen\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
            r"aiohttp\.ClientSession\(\)\.post\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct HTTP requests to LLM providers bypass the sovereign gateway. "
                       "Use from shared.llm import get_llm_client — the ONLY path to intelligence.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "subprocess_ollama_model_access": {
        "patterns": [
            r"subprocess\.run\(\s*\[\s*[\"']ollama[\"']\s*,\s*[\"']run[\"']",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: subprocess ollama run bypasses the sovereign gateway. "
                       "ollama pull is permitted (infrastructure provisioning). ollama run is forbidden (model access). "
                       "Use shared/llm/client.py for all model access.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "llm_manager_bypass": {
        "patterns": [
            r"from\s+core\.llm_manager\s+import",
            r"from\s+core\.llm\.manager\s+import",
        ],
        "why_blocked": "DEPRECATED: core/llm_manager.py and core/llm/manager.py are now adapters to the sovereign gateway. "
                       "Import from shared.llm directly — the single point of model access.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
}


class ForbiddenPatternDetector:
    
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


# =============================================================================
# PRE-EXECUTION GATE (Now checks task + validates actual injection)
# =============================================================================

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
    
    def __init__(self, reference_dir: Path):
        self.reference_dir = reference_dir
        self.pattern_detector = ForbiddenPatternDetector()
    
    def validate(self, context: ExecutionContext) -> EnforcementResult:
        result = EnforcementResult(gate_result=GateResult.PASS)
        
        # 1. Check mandatory references actually loaded (not just exist)
        missing_mandatory = self._check_mandatory_loaded(context)
        if missing_mandatory:
            result.missing_references.extend(missing_mandatory)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"Mandatory references not loaded into context: {missing_mandatory}")
        
        # 2. Scan task for forbidden patterns (PRE-EXECUTION)
        task_patterns = self.pattern_detector.scan_task(context.task)
        if task_patterns:
            for pattern_name in task_patterns:
                pattern_def = FORBIDDEN_PATTERNS[pattern_name]
                result.missing_references.extend(pattern_def["mandatory_retrieval"])
                result.violations.append(
                    f"Task contains pattern '{pattern_name}': {pattern_def['why_blocked']}. "
                    f"Reference retrieval enforced."
                )
        
        # 3. Verify references are actually loaded with content
        missing_loaded = self._check_references_actually_loaded(context)
        if missing_loaded:
            result.missing_references.extend(missing_loaded)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"References exist but not loaded into context: {missing_loaded}")
        
        # 4. Check domain safety gates
        domain_missing = self._check_domain_safety(context)
        if domain_missing:
            result.missing_references.extend(domain_missing)
            result.gate_result = GateResult.BLOCK
            result.violations.append(f"Domain safety references not loaded: {domain_missing}")
        
        return result
    
    def _check_mandatory_loaded(self, context: ExecutionContext) -> List[str]:
        """Check that mandatory references are in loaded_references with content."""
        missing = []
        loaded_paths = {str(r.path.name) for r in context.loaded_references}
        
        for ref in MANDATORY_REFERENCES:
            if ref not in loaded_paths:
                # Check if it exists on disk but wasn't loaded
                full_path = self.reference_dir / ref
                if full_path.exists():
                    missing.append(f"{ref} (exists on disk but NOT loaded into context)")
                else:
                    missing.append(f"{ref} (MISSING from disk)")
        return missing
    
    def _check_references_actually_loaded(self, context: ExecutionContext) -> List[str]:
        """Verify each retrieved reference has actual content loaded."""
        missing = []
        for ref_path in context.retrieved_reference_paths:
            loaded = any(
                r.path == ref_path and r.content.strip()
                for r in context.loaded_references
            )
            if not loaded:
                missing.append(str(ref_path))
        return missing
    
    def _check_domain_safety(self, context: ExecutionContext) -> List[str]:
        """Check domain safety references are loaded with content."""
        missing = []
        loaded_paths = {str(r.path) for r in context.loaded_references}
        
        for domain in context.triggered_domains:
            if domain in DOMAIN_SAFETY_RULES:
                for required_ref in DOMAIN_SAFETY_RULES[domain]:
                    # Check if any loaded reference path contains this required path
                    found = any(required_ref in str(p) for p in loaded_paths)
                    if not found:
                        missing.append(required_ref)
        return missing


# =============================================================================
# POST-EXECUTION GATE
# =============================================================================

class PostExecutionGate:
    
    def __init__(self, reference_dir: Path):
        self.reference_dir = reference_dir
        self.pattern_detector = ForbiddenPatternDetector()
    
    def validate(self, context: ExecutionContext) -> EnforcementResult:
        result = EnforcementResult(gate_result=GateResult.PASS)
        
        # 1. Scan for forbidden patterns in response
        forbidden_result = self.pattern_detector.scan_response(context)
        if forbidden_result.gate_result == GateResult.BLOCK:
            result.gate_result = GateResult.BLOCK
            result.forbidden_patterns = forbidden_result.forbidden_patterns
            result.missing_references = forbidden_result.missing_references
            result.violations.append(f"Forbidden patterns in response: {forbidden_result.forbidden_patterns}")
            return result
        
        # 2. Classify confidence
        result.confidence = self._classify_confidence(context)
        
        # 3. Check escalation
        if self._should_escalate(context, result.confidence):
            result.gate_result = GateResult.ESCALATE
            result.escalation_reason = f"UNTESTED recommendation in critical domain"
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
        critical_domains = {
            "financial", "security", "architecture", "money", "payment",
            "banking", "auth", "encryption", "vulnerability", "scale"
        }
        return bool(context.triggered_domains & critical_domains)
    
    def _determine_escalation_domain(self, context: ExecutionContext) -> str:
        domain_map = {
            "financial": "FINANCIAL", "money": "FINANCIAL", "payment": "FINANCIAL",
            "banking": "FINANCIAL", "transaction": "FINANCIAL",
            "security": "SECURITY", "auth": "SECURITY", "encryption": "SECURITY",
            "vulnerability": "SECURITY",
            "architecture": "ARCHITECTURE", "scale": "ARCHITECTURE",
        }
        for domain in sorted(context.triggered_domains):
            if domain in domain_map:
                return domain_map[domain]
        return "UNKNOWN"


# =============================================================================
# ENFORCEMENT ENGINE (With recursion guard)
# =============================================================================

class EnforcementEngine:
    """Fail-closed enforcement engine with recursion guard and audit trail."""
    
    def __init__(self, reference_dir: Path):
        self.reference_dir = Path(reference_dir)
        self.pre_gate = PreExecutionGate(self.reference_dir)
        self.post_gate = PostExecutionGate(self.reference_dir)
        self.pattern_detector = ForbiddenPatternDetector()
        self.audit = AuditTrail(self.reference_dir)
        self.max_attempts = MAX_ENFORCEMENT_ATTEMPTS
    
    def load_reference(self, ref_path: Path) -> LoadedReference:
        """Load a reference file and return a LoadedReference with content hash."""
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference not found: {ref_path}")
        
        content = ref_path.read_text(encoding='utf-8')
        return LoadedReference(
            path=ref_path,
            content=content,
            size_bytes=len(content.encode('utf-8')),
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            loaded_at=datetime.now(timezone.utc)
        )
    
    def force_load_references(self, context: ExecutionContext, ref_names: List[str]):
        """Force-load references into context with actual content."""
        for ref_name in ref_names:
            full_path = self.reference_dir / ref_name
            if full_path.exists():
                # Check if already loaded
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
        """
        Main execution pipeline. Recursion-guarded enforcement.
        
        Args:
            context: ExecutionContext with task and triggered domains
            llm_call_fn: Callable that takes context and returns response string
            attempt: Current enforcement attempt (1-based, max MAX_ENFORCEMENT_ATTEMPTS)
        
        Returns:
            EnforcementResult with gate outcomes, confidence, and violations
        """
        context.enforcement_attempts = attempt
        
        # ===== RECURSION GUARD =====
        if attempt > self.max_attempts:
            self.audit.append("FATAL_MAX_ATTEMPTS", {
                "task": context.task[:500],
                "attempts": attempt,
                "triggered_domains": list(context.triggered_domains),
            })
            return EnforcementResult(
                gate_result=GateResult.FATAL,
                attempt_number=attempt,
                violations=[
                    f"Maximum enforcement attempts ({self.max_attempts}) exceeded. "
                    "Human intervention required."
                ],
                escalation_reason="Repeated governance failure - system cannot resolve",
                escalation_domain="SYSTEM"
            )
        
        # ===== PRE-EXECUTION GATE =====
        self.audit.append("PRE_GATE_START", {
            "task": context.task[:500],
            "attempt": attempt,
            "domains": list(context.triggered_domains),
        })
        
        pre_result = self.pre_gate.validate(context)
        
        if pre_result.gate_result == GateResult.BLOCK:
            self.audit.append("PRE_GATE_BLOCK", {
                "violations": pre_result.violations,
                "missing_refs": pre_result.missing_references,
                "attempt": attempt,
            })
            
            # Force retrieval of missing references WITH ACTUAL CONTENT
            self.force_load_references(context, pre_result.missing_references)
            
            # Recurse with incremented attempt
            return self.execute_with_enforcement(context, llm_call_fn, attempt + 1)
        
        # ===== LLM EXECUTION =====
        self.audit.append("LLM_EXECUTION_START", {
            "attempt": attempt,
            "loaded_ref_count": len(context.loaded_references),
        })
        
        try:
            context.llm_response = llm_call_fn(context)
        except Exception as e:
            self.audit.append("LLM_EXECUTION_FAILURE", {
                "error": str(e),
                "attempt": attempt,
            })
            return EnforcementResult(
                gate_result=GateResult.BLOCK,
                attempt_number=attempt,
                violations=[f"LLM execution failed: {str(e)}"]
            )
        
        # ===== POST-EXECUTION GATE =====
        self.audit.append("POST_GATE_START", {
            "attempt": attempt,
            "response_length": len(context.llm_response) if context.llm_response else 0,
        })
        
        post_result = self.post_gate.validate(context)
        post_result.attempt_number = attempt
        
        if post_result.gate_result == GateResult.BLOCK:
            self.audit.append("POST_GATE_BLOCK", {
                "violations": post_result.violations,
                "forbidden_patterns": post_result.forbidden_patterns,
                "missing_refs": post_result.missing_references,
                "attempt": attempt,
            })
            
            # Force retrieval and retry
            self.force_load_references(context, post_result.missing_references)
            return self.execute_with_enforcement(context, llm_call_fn, attempt + 1)
        
        if post_result.gate_result == GateResult.ESCALATE:
            self.audit.append("ESCALATION", {
                "domain": post_result.escalation_domain,
                "reason": post_result.escalation_reason,
                "confidence": post_result.confidence.value,
            })
            context.llm_response = self._inject_escalation_warning(
                context.llm_response, post_result
            )
        
        # ===== CONFIDENCE WARNING =====
        if post_result.confidence == ConfidenceLevel.UNTESTED:
            context.llm_response = self._inject_confidence_warning(context.llm_response)
        
        # ===== SUCCESS =====
        self.audit.append("EXECUTION_COMPLETE", {
            "attempt": attempt,
            "gate": post_result.gate_result.value,
            "confidence": post_result.confidence.value,
        })
        
        return post_result
    
    def _inject_escalation_warning(self, response: str, result: EnforcementResult) -> str:
        return f"""🔴 ESCALATION REQUIRED
Domain: {result.escalation_domain}
Reason: {result.escalation_reason}
Risk: This recommendation has not been validated against production incidents.
Action Required: Human review before implementation.

---
{response}"""
    
    def _inject_confidence_warning(self, response: str) -> str:
        return """⚠️ CONFIDENCE: UNTESTED
This recommendation has not been validated against production incidents.
No truth_sources entry confirms or denies this approach.
Consider:
1. Testing in isolation before production use
2. Adding findings to truth_sources/ after validation
3. Reviewing if a VALIDATED alternative exists

---
""" + response


# =============================================================================
# OUTCOME LOGGER (Decision Feedback Loop Integration)
# =============================================================================

class OutcomeLogger:
    
    def __init__(self, reference_dir: Path):
        self.reference_dir = Path(reference_dir)
        self.audit = AuditTrail(reference_dir)
    
    def record_outcome(self, context: ExecutionContext, result: EnforcementResult, actual_outcome: str = None):
        self.audit.append("DECISION_OUTCOME", {
            "task": context.task[:500],
            "domains": list(context.triggered_domains),
            "confidence": result.confidence.value,
            "gate_result": result.gate_result.value,
            "attempts": result.attempt_number,
            "loaded_refs": [str(r.path) for r in context.loaded_references],
            "violations": result.violations,
            "actual_outcome": actual_outcome or "Not yet recorded",
        })
    
    def record_failure(self, context: ExecutionContext, result: EnforcementResult, failure_description: str):
        self.audit.append("FAILURE_POSTMORTEM", {
            "task": context.task[:500],
            "failure": failure_description,
            "domains": list(context.triggered_domains),
            "confidence": result.confidence.value,
            "gate_result": result.gate_result.value,
            "violations": result.violations,
            "forbidden_patterns": result.forbidden_patterns,
        })


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    reference_dir = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references/claw_coder")
    engine = EnforcementEngine(reference_dir)
    logger = OutcomeLogger(reference_dir)
    
    # Verify audit integrity
    if not engine.audit.verify_integrity():
        print("⚠️ AUDIT TRAIL INTEGRITY FAILURE")
        exit(1)
    
    context = ExecutionContext(
        task="Build a high-scale payment processing system - we should rewrite everything from scratch",
        triggered_domains={"financial", "payment", "scale", "architecture", "transaction"},
    )
    
    # The task itself contains "rewrite everything from scratch" - pre-gate will catch this
    
    def llm_call(ctx: ExecutionContext) -> str:
        return """We should rebuild this from scratch using microservices.
The new framework handles all the security concerns.
We'll add compliance later - it's not critical for MVP."""

    result = engine.execute_with_enforcement(context, llm_call)
    
    print(f"Gate Result: {result.gate_result.value}")
    print(f"Attempt: {result.attempt_number}")
    print(f"Confidence: {result.confidence.value}")
    print(f"Violations: {result.violations}")
    print(f"Forbidden Patterns: {result.forbidden_patterns}")
    
    if result.gate_result == GateResult.BLOCK:
        logger.record_failure(context, result, "Response blocked due to forbidden patterns")
    else:
        logger.record_outcome(context, result)
    
    print(f"\nAudit integrity: {engine.audit.verify_integrity()}")