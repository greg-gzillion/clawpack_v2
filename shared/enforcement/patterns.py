"""Forbidden patterns — engineering anti-patterns and constitutional sovereignty violations."""

# =============================================================================
# ENGINEERING PATTERNS — Prevent bad technical decisions
# =============================================================================

ENGINEERING_PATTERNS = {
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
        "check_task": True,
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
    },
}

# =============================================================================
# LLM SOVEREIGNTY PATTERNS — Constitutional Law
# =============================================================================

SOVEREIGNTY_PATTERNS = {
    "direct_ollama_import": {
        "patterns": [
            r"import\s+ollama",
            r"from\s+ollama\s+import",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. All model access must route through shared/llm/client.py — the sovereign gateway.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_groq_import": {
        "patterns": [
            r"from\s+groq\s+import",
            r"import\s+groq",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. All model access must route through shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_openrouter_call": {
        "patterns": [
            r"openrouter\.ai",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct OpenRouter API calls bypass the sovereign gateway. Use shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_groq_api_call": {
        "patterns": [
            r"api\.groq\.com",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct Groq API calls bypass the sovereign gateway. Use shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_ollama_http": {
        "patterns": [
            r"localhost:11434",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct Ollama HTTP calls bypass the sovereign gateway. Use shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_anthropic_import": {
        "patterns": [
            r"import\s+anthropic",
            r"from\s+anthropic\s+import",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: No agent may speak to a model directly. All model access must route through shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "direct_provider_request": {
        "patterns": [
            r"requests\.post\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
            r"urllib\.request\.urlopen\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
            r"aiohttp\.ClientSession\(\)\.post\(\s*[\"']https?://(api\.openai|api\.anthropic|openrouter\.ai|api\.groq)",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: Direct HTTP requests to LLM providers bypass the sovereign gateway. Use from shared.llm import get_llm_client.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "subprocess_ollama_model_access": {
        "patterns": [
            r"subprocess\.run\(\s*\[\s*[\"']ollama[\"']\s*,\s*[\"']run[\"']",
        ],
        "why_blocked": "CONSTITUTIONAL VIOLATION: subprocess ollama run bypasses the sovereign gateway. ollama pull is permitted (infrastructure provisioning). ollama run is forbidden (model access). Use shared/llm/client.py.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
    "llm_manager_bypass": {
        "patterns": [
            r"from\s+core\.llm_manager\s+import",
            r"from\s+core\.llm\.manager\s+import",
        ],
        "why_blocked": "DEPRECATED: core/llm_manager.py and core/llm/manager.py are now adapters to the sovereign gateway. Import from shared.llm directly.",
        "mandatory_retrieval": ["OPERATING_RULES.md"],
        "check_task": True,
    },
}

# Combined patterns for the detector
FORBIDDEN_PATTERNS = {**ENGINEERING_PATTERNS, **SOVEREIGNTY_PATTERNS}

__all__ = ['ENGINEERING_PATTERNS', 'SOVEREIGNTY_PATTERNS', 'FORBIDDEN_PATTERNS']