# shared/capabilities.py
"""
Constitutional Capability Registry — the canonical map of which agent owns which capability.

Article II: Every agent has defined jurisdiction. No crossing.
This registry enforces that by mapping capabilities to their constitutional owner.

Any agent can resolve any capability. The agent doesn't gain the capability —
it recognizes it belongs to another ministry and delegates.
"""
from typing import Optional

CAPABILITIES = {
    # Document Ministry
    "doc": "docuclaw",
    "draft": "docuclaw",
    "create": "docuclaw",
    "letter": "docuclaw",
    "report": "docuclaw",
    "memo": "docuclaw",
    
    # Visualization Ministry
    "plot": "plotclaw",
    "chart": "plotclaw",
    "graph": "plotclaw",
    "bar": "plotclaw",
    "line": "plotclaw",
    "scatter": "plotclaw",
    "pie": "plotclaw",
    
    # Diagram Ministry
    "flow": "flowclaw",
    "flowchart": "flowclaw",
    "diagram": "flowclaw",
    "mindmap": "flowclaw",
    
    # Design Ministry
    "design": "designclaw",
    "brand": "designclaw",
    "logo": "designclaw",
    
    # Draft Ministry
    "blueprint": "draftclaw",
    "permit": "draftclaw",
    "structural": "draftclaw",
    "cad": "draftclaw",
    
    # Code Ministry
    "code": "claw_coder",
    "debug": "claw_coder",
    "review": "claw_coder",
    
    # Math Ministry
    "math": "mathematicaclaw",
    "solve": "mathematicaclaw",
    "derivative": "mathematicaclaw",
    "integral": "mathematicaclaw",
    
    # File Ministry
    "file": "fileclaw",
    "export": "fileclaw",
    "convert": "fileclaw",
    
    # Translation Ministry
    "translate": "interpretclaw",
    "interpret": "interpretclaw",
    
    # Draw Ministry
    "draw": "drawclaw",
    "paint": "drawclaw",
    "sketch": "drawclaw",
    
    # Web Ministry
    "web": "webclaw",
    "search": "webclaw",
    "fetch": "webclaw",
    
    # Data Ministry
    "data": "dataclaw",
    
    # Law Ministry
    "law": "lawclaw",
    "court": "lawclaw",
    "docket": "lawclaw",
    "jurisdiction": "lawclaw",
    "precedent": "lawclaw",
    "statute": "lawclaw",
    
    # Medical Ministry
    "medical": "mediclaw",
    "diagnose": "mediclaw",
    "treatment": "mediclaw",
    
    # TX Ministry
    "tx": "txclaw",
    "blockchain": "txclaw",
    
    # Rust Ministry
    "rust": "crustyclaw",
    "audit": "crustyclaw",
    
    # Liberation Ministry
    "liberate": "liberateclaw",
    "obliterate": "liberateclaw",
}


def resolve_capability(command: str) -> Optional[str]:
    """
    Given a command like '/plot' or 'plot', return the agent that owns it.
    Returns None if no agent owns this capability.
    
    Constitutional: this does not give the calling agent new powers.
    It identifies the proper ministry for delegation.
    """
    cmd = command.lower().lstrip("/").split()[0] if command else ""
    return CAPABILITIES.get(cmd)


def get_capable_agent(command: str, caller: str) -> Optional[str]:
    """
    Resolve capability and check that caller isn't routing to itself.
    Returns agent name or None.
    """
    target = resolve_capability(command)
    if target and target != caller:
        return target
    return None