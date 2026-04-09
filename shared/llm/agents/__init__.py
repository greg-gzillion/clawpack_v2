"""Agent LLM Factory - All clawpack agents"""

from .interpretclaw import InterpretClawLLM
from .lawclaw import LawClawLLM
from .clawcoder import ClawCoderLLM
from .webclaw import WebClawLLM
from .mediclaw import MedicLawLLM
from .txclaw import TxClawLLM
from .dataclaw import DataClawLLM
from .docuclaw import DocuClawLLM
from .mathematicaclaw import MathematicaLawLLM
from .langclaw import LangClawLLM

class AgentLLMFactory:
    _agents = {
        "interpretclaw": InterpretClawLLM,
        "lawclaw": LawClawLLM,
        "claw_coder": ClawCoderLLM,
        "webclaw": WebClawLLM,
        "mediclaw": MedicLawLLM,
        "txclaw": TxClawLLM,
        "dataclaw": DataClawLLM,
        "docuclaw": DocuClawLLM,
        "mathematicaclaw": MathematicaLawLLM,
        "langclaw": LangClawLLM
    }
    
    @classmethod
    def get(cls, agent_name: str):
        agent_class = cls._agents.get(agent_name.lower())
        if agent_class:
            return agent_class()
        return None
    
    @classmethod
    def list_agents(cls):
        return list(cls._agents.keys())
    
    @classmethod
    def get_all(cls):
        """Get all agent LLM instances"""
        return {name: cls.get(name) for name in cls._agents}
