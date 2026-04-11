"""AI-Powered Math Visualizer - Uses LLM"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import webbrowser
import hashlib

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class AIVisualizer:
    def __init__(self):
        self.llm = None
        self._init_llm()
    
    def _init_llm(self):
        try:
            from core.llm_manager import get_llm_manager
            self.llm = get_llm_manager()
            if self.llm and self.llm.groq_client:
                print("✅ LLM connected for visualization", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ LLM error: {e}", file=sys.stderr)
    
    def visualize(self, request: str) -> str:
        """Use LLM to interpret and generate visualization"""
        
        if not self.llm:
            return "❌ LLM not connected. Please check GROQ_API_KEY in .env"
        
        # Ask LLM to generate the visualization code
        prompt = f"""Generate Python code to visualize: {request}

Requirements:
- Use matplotlib and numpy
- Create a beautiful visualization
- Save to 'plot.png'
- Use proper labels and title

Return ONLY the Python code, no explanations."""

        try:
            response = self.llm.chat_sync(prompt, task_type="code")
            # Extract code from response
            code = response.replace('```python', '').replace('```', '').strip()
            
            # Execute the generated code
            exec_globals = {'np': np, 'plt': plt}
            exec(code, exec_globals)
            
            # Save the plot
            output_dir = Path.home() / ".clawpack" / "plots"
            output_dir.mkdir(parents=True, exist_ok=True)
            hash_id = hashlib.md5(request.encode()).hexdigest()[:8]
            output_file = output_dir / f"plot_{hash_id}.png"
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            webbrowser.open(f'file://{output_file}')
            
            return f"✅ AI visualization for: {request}\n📁 Saved: {output_file}\n🌐 Browser opened"
            
        except Exception as e:
            return f"❌ AI visualization error: {e}\n\nTry simpler description like: 'sine wave', 'parabola', '3D surface'"

ai_visualizer = AIVisualizer()
