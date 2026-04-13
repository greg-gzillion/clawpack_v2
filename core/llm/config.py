"""Task Configuration"""

TASK_MAP = {
    "code": ["deepseek-coder:6.7b", "codellama:7b", "qwen3-coder:30b"],
    "general": ["gemma3:4b", "tinyllama:1.1b"],
    "reasoning": ["deepseek-r1:8b", "gemma3:12b", "qwen3-vl:30b"],
    "creative": ["gemma3:12b", "gemma3:4b"],
}

AGENT_TASKS = {
    "claw_coder": "code",
    "txclaw": "code",
    "rustypycraw": "code",
    "lawclaw": "reasoning",
    "mediclaw": "reasoning",
    "mathematicaclaw": "reasoning",
    "flowclaw": "creative",
    "designclaw": "creative",
    "docuclaw": "general",
}

AGENT_MODEL_OVERRIDES = {
    "claw_coder": ["qwen3-coder:30b", "deepseek-coder:6.7b", "codellama:7b"],
    "rustypycraw": ["codellama:7b", "deepseek-coder:6.7b"],
    "txclaw": ["deepseek-coder:6.7b", "codellama:7b"],
}

def get_task_for_agent(agent: str) -> str:
    return AGENT_TASKS.get(agent, "general")

def get_models_for_task(task: str) -> list:
    return TASK_MAP.get(task, TASK_MAP["general"])

def get_models_for_agent(agent: str) -> list:
    if agent in AGENT_MODEL_OVERRIDES:
        return AGENT_MODEL_OVERRIDES[agent]
    return get_models_for_task(get_task_for_agent(agent))
