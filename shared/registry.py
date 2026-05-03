"""Agent Registry & Delegation Layer

   Every agent registers its capabilities. Any agent can delegate tasks
   to specialized agents. This is the internal constitution of offices.
"""
from typing import Dict, List, Optional

AGENT_REGISTRY: Dict[str, Dict] = {
    "docuclaw": {
        "domain": "Document Creation & Structuring",
        "icon": "📄",
        "capabilities": [
            "create_document", "create_contract", "create_legal_brief",
            "create_medical_report", "create_math_paper", "create_proposal",
            "create_letter", "create_report", "import_csv", "import_json",
            "export_document",
        ],
        "templates": {
            "lawclaw": ["contract", "legal_brief", "motion"],
            "mediclaw": ["medical_report", "prescription"],
            "mathematicaclaw": ["math_paper", "math_solution"],
            "txclaw": ["deployment_plan"],
            "draftclaw": ["proposal", "letter"],
            "claw_coder": ["readme"],
            "webclaw": ["report"],
            "docuclaw": ["letter", "report", "meeting_notes"],
        },
    },
    "fileclaw": {
        "domain": "File Format Conversion & Operations",
        "icon": "📁",
        "capabilities": ["convert_file", "analyze_file", "batch_process", "find_files", "detect_type", "calculate_hash"],
    },
    "drawclaw": {
        "domain": "Visual Art & Illustration",
        "icon": "🎨",
        "capabilities": ["draw", "sketch", "illustrate", "paint", "doodle", "cartoon", "compose", "animate"],
    },
    "plotclaw": {
        "domain": "Data Visualization & Plots",
        "icon": "📊",
        "capabilities": ["plot", "bar_chart", "pie_chart", "line_graph", "scatter_plot", "histogram"],
    },
    "webclaw": {
        "domain": "Web Search & References",
        "icon": "🌐",
        "capabilities": ["search_web", "fetch_url", "search_references", "search_chronicle", "cite_source"],
    },
    "lawclaw": {
        "domain": "Legal Analysis & Research",
        "icon": "⚖️",
        "capabilities": ["legal_research", "analyze_case", "search_statute", "analyze_contract"],
    },
    "mediclaw": {
        "domain": "Medical Analysis",
        "icon": "🏥",
        "capabilities": ["analyze_symptoms", "diagnose", "research_treatment", "check_interactions"],
    },
    "mathematicaclaw": {
        "domain": "Mathematics & Computation",
        "icon": "📐",
        "capabilities": ["solve_equation", "derivative", "integral", "plot_function", "compute"],
    },
    "claw_coder": {
        "domain": "Code Generation & Engineering",
        "icon": "💻",
        "capabilities": ["generate_code", "review_code", "debug", "explain_code", "refactor", "write_tests"],
    },
    "dataclaw": {
        "domain": "Data Processing & Analysis",
        "icon": "📊",
        "capabilities": ["process_data", "analyze_dataset", "search_data", "index_data", "export_data"],
    }

    "draftclaw": {
        "domain": "Technical Drawing, Permit Review & Jurisdiction Intelligence",
        "icon": "📐",
        "capabilities": [
            "jurisdiction_lookup",
            "permit_review",
            "commercial_plan_check",
            "occupancy_classification",
            "ahj_contact_resolution",
            "design_criteria_extraction",
            "code_compliance_check",
            "audit_jurisdictions",
            "score_confidence",
        ],
        "templates": {
            "docuclaw": ["proposal", "letter", "permit_packet"],
        },
    },
,
    "txclaw": {
        "domain": "Transaction & Deployment",
        "icon": "💎",
        "capabilities": ["deploy_contract", "verify_network", "check_tx_status", "generate_reference"],
    },
    "flowclaw": {
        "domain": "Diagrams & Flowcharts",
        "icon": "🔄",
        "capabilities": ["create_flowchart", "create_mindmap", "create_diagram", "create_sequence"],
    },
    "langclaw": {
        "domain": "Language Teaching & Learning",
        "icon": "🗣",
        "capabilities": [
            "teach_language", "language_lesson", "practice_exercises",
            "vocabulary", "conversation_practice", "pronunciation",
        ],
    },
    "interpretclaw": {
        "domain": "Translation & Interpretation",
        "icon": "🌍",
        "capabilities": ["translate", "detect_language", "interpret", "transcribe"],
    },
    "llmclaw": {
        "domain": "Model Management & Orchestration",
        "icon": "🧠",
        "capabilities": ["list_models", "use_model", "orchestrate", "get_stats"],
    },
}

CAPABILITY_MAP: Dict[str, str] = {}
for agent_name, agent_info in AGENT_REGISTRY.items():
    for cap in agent_info["capabilities"]:
        CAPABILITY_MAP[cap] = agent_name

DOMAIN_SHORTCUTS = {
    "document": "docuclaw", "contract": "docuclaw", "brief": "docuclaw",
    "file": "fileclaw", "convert": "fileclaw",
    "draw": "drawclaw", "art": "drawclaw", "illustration": "drawclaw",
    "plot": "plotclaw", "chart": "plotclaw", "graph": "plotclaw",
    "search": "webclaw", "reference": "webclaw", "web": "webclaw",
    "legal": "lawclaw", "law": "lawclaw",
    "medical": "mediclaw", "health": "mediclaw",
    "math": "mathematicaclaw", "equation": "mathematicaclaw",
    "code": "claw_coder", "programming": "claw_coder",
    "data": "dataclaw", "analysis": "dataclaw",
    "deploy": "txclaw", "tx": "txclaw", "transaction": "txclaw",
    "flowchart": "flowclaw", "diagram": "flowclaw", "mindmap": "flowclaw",
    "translate": "interpretclaw", "language": "interpretclaw",
    "model": "llmclaw", "orchestrate": "llmclaw",
    "language": "langclaw", "lesson": "langclaw", "teach": "langclaw",
    "translate": "interpretclaw", "detect_lang": "interpretclaw",
}

def get_all_agents() -> List[str]:
    return list(AGENT_REGISTRY.keys())

def get_capabilities(agent: str = None) -> Dict:
    if agent:
        return AGENT_REGISTRY.get(agent, {})
    return AGENT_REGISTRY

def find_agent_for(task: str) -> Optional[str]:
    if task in CAPABILITY_MAP:
        return CAPABILITY_MAP[task]
    if task in DOMAIN_SHORTCUTS:
        return DOMAIN_SHORTCUTS[task]
    return None

def get_agent_info(agent: str) -> Dict:
    return AGENT_REGISTRY.get(agent, {})

def get_templates_for_agent(agent: str) -> List[str]:
    docuclaw = AGENT_REGISTRY.get("docuclaw", {})
    return docuclaw.get("templates", {}).get(agent, [])

def delegate(calling_agent: str, capability: str, **kwargs) -> Dict:
    target = find_agent_for(capability)
    if not target:
        return {
            "status": "error",
            "error": f"No agent found for: {capability}",
            "available": list(CAPABILITY_MAP.keys())[:15],
        }
    try:
        if target == "docuclaw":
            from shared.docuclaw_api import create_for_agent
            template = kwargs.get("template", "letter")
            values = kwargs.get("values", {})
            return create_for_agent(calling_agent, template, values)
        elif target == "fileclaw":
            from shared.files import convert_file, analyze_file, find_files
            op = kwargs.get("operation", "analyze")
            if op == "convert":
                return convert_file(kwargs.get("input_path", ""), kwargs.get("target_format", "txt"))
            elif op == "find":
                return {"status": "success", "results": find_files(kwargs.get("query", ""))}
            else:
                return analyze_file(kwargs.get("input_path", ""), use_ai=True)
        elif target == "langclaw":
            return {
                "status": "delegated",
                "to_agent": "langclaw",
                "domain": "Language Teaching",
                "capability": capability,
                "note": "Task routed to langclaw for language teaching. Use /lesson, /practice, /vocab.",
            }
        elif target == "interpretclaw":
            return {
                "status": "delegated",
                "to_agent": "interpretclaw", 
                "domain": "Translation & Interpretation",
                "capability": capability,
                "note": "Task routed to interpretclaw for translation. Use /translate, /detect.",
            }
        elif target == "webclaw":
            from shared.memory.unified_memory import get_memory
            memory = get_memory()
            results = memory.search_chronicle(kwargs.get("query", ""), limit=10)
            return {"status": "success", "agent": "webclaw", "results": results, "count": len(results)}
        else:
            return {
                "status": "delegated",
                "to_agent": target,
                "domain": get_agent_info(target).get("domain", ""),
                "capability": capability,
                "note": f"Task routed to {target}. Full delegation via A2A pending.",
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "to_agent": target}

__all__ = [
    "AGENT_REGISTRY", "CAPABILITY_MAP", "DOMAIN_SHORTCUTS",
    "get_all_agents", "get_capabilities", "find_agent_for",
    "get_agent_info", "get_templates_for_agent", "delegate",
]