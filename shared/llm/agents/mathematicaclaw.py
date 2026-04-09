"""MathematicaLaw LLM Agent - Math problem solving and explanation"""
from .. import get_llm

class MathematicaLawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def solve_problem(self, problem: str, subject: str = "general") -> str:
        """Solve math problems with step-by-step explanation"""
        prompt = f"Solve this {subject} math problem step-by-step:\n\n{problem}\n\nShow work and explain each step."
        return self.llm.generate(prompt, task="general").text
    
    def explain_concept(self, concept: str, level: str = "intermediate") -> str:
        """Explain mathematical concepts"""
        prompt = f"Explain '{concept}' at {level} level. Include definition, examples, and applications."
        return self.llm.generate(prompt, task="general").text
    
    def derive_formula(self, formula: str) -> str:
        """Derive a mathematical formula"""
        prompt = f"Derive the formula for {formula} step-by-step. Include assumptions and key insights."
        return self.llm.generate(prompt, task="general").text
    
    def prove_theorem(self, theorem: str) -> str:
        """Prove a mathematical theorem"""
        prompt = f"Prove the theorem: {theorem}. Include lemmas and logical steps."
        return self.llm.generate(prompt, task="general").text
    
    def optimize_calculation(self, calculation: str, method: str = "efficient") -> str:
        """Optimize mathematical calculations"""
        prompt = f"Optimize this calculation using {method} methods:\n\n{calculation}"
        return self.llm.generate(prompt, task="general").text
    
    def generate_practice(self, topic: str, difficulty: str = "medium", num_problems: int = 5) -> str:
        """Generate practice problems"""
        prompt = f"Generate {num_problems} {difficulty} practice problems about {topic}. Include answers and explanations."
        return self.llm.generate(prompt, task="general").text
