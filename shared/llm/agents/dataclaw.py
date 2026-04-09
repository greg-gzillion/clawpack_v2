"""DataClaw LLM Agent - Data analysis and processing"""
from .. import get_llm

class DataClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def analyze_data(self, data_description: str, analysis_type: str = "descriptive") -> str:
        """Analyze data and provide insights"""
        prompt = f"Perform {analysis_type} analysis on this data: {data_description}. Provide key insights and patterns."
        return self.llm.generate(prompt, task="general").text
    
    def generate_sql(self, question: str, schema: str = "") -> str:
        """Generate SQL queries from natural language"""
        prompt = f"Generate SQL query for: {question}\nSchema: {schema}"
        return self.llm.generate(prompt, task="code").text
    
    def explain_statistics(self, concept: str, level: str = "beginner") -> str:
        """Explain statistical concepts"""
        prompt = f"Explain '{concept}' statistics at {level} level. Include examples and applications."
        return self.llm.generate(prompt, task="general").text
    
    def data_cleaning(self, data_issues: str) -> str:
        """Recommend data cleaning strategies"""
        prompt = f"Recommend data cleaning strategies for: {data_issues}. Include steps and best practices."
        return self.llm.generate(prompt, task="general").text
    
    def choose_algorithm(self, problem_type: str, constraints: str) -> str:
        """Recommend machine learning algorithms"""
        prompt = f"Recommend ML algorithms for {problem_type} with constraints: {constraints}. Include pros/cons."
        return self.llm.generate(prompt, task="general").text
    
    def visualize_suggestion(self, data_type: str, goal: str) -> str:
        """Suggest visualization types"""
        prompt = f"Suggest best visualization types for {data_type} data to achieve: {goal}. Include library recommendations."
        return self.llm.generate(prompt, task="general").text
