"""WebClaw LLM Agent - Web content summarization and research"""
from .. import get_llm

class WebClawLLM:
    def __init__(self):
        self.llm = get_llm()
    
    def summarize(self, content: str, max_points: int = 5) -> str:
        """Summarize web content into key points"""
        prompt = f"Summarize this web content into {max_points} key points:\n\n{content}"
        return self.llm.generate(prompt, task="research").text
    
    def research(self, topic: str, context: str = "") -> str:
        """Research a topic and provide comprehensive information"""
        prompt = f"Research topic: {topic}\nContext: {context}\nProvide comprehensive information with key findings."
        return self.llm.generate(prompt, task="research").text
    
    def extract_insights(self, content: str, focus: str = "general") -> str:
        """Extract specific insights from content"""
        prompt = f"Extract key insights related to {focus} from:\n\n{content}"
        return self.llm.generate(prompt, task="research").text
    
    def compare_sources(self, source1: str, source2: str, criteria: str = "accuracy") -> str:
        """Compare two sources of information"""
        prompt = f"Compare these two sources based on {criteria}:\n\nSource A: {source1}\n\nSource B: {source2}"
        return self.llm.generate(prompt, task="research").text
    
    def detect_bias(self, content: str) -> str:
        """Detect potential bias in content"""
        prompt = f"Analyze this content for potential bias, partiality, or missing perspectives:\n\n{content}"
        return self.llm.generate(prompt, task="general").text
    
    def generate_questions(self, content: str, num_questions: int = 5) -> str:
        """Generate research questions from content"""
        prompt = f"Generate {num_questions} research questions based on this content:\n\n{content}"
        return self.llm.generate(prompt, task="general").text
