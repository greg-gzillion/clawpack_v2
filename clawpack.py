#!/usr/bin/env python3
"""CLAWPACK - Unified Agent Router"""
import sys
import subprocess
from pathlib import Path

class Clawpack:
    def __init__(self):
        self.agents_path = Path("agents")
        self.agent_map = {
            "translate": {"agent": "interpretclaw", "cmd": "translate {text} to {target}"},
            "math": {"agent": "mathematicaclaw", "cmd": "solve {equation}"},
            "plot": {"agent": "plotclaw", "cmd": "plot {expression}"},
            "dream": {"agent": "dreamclaw", "cmd": "dream {prompt}"},
            "flowchart": {"agent": "flowclaw", "cmd": "flowchart {steps}"},
        }
    
    def route(self, user_input: str) -> tuple:
        text = user_input.lower()
        
        if "translate" in text and " to " in text:
            parts = user_input.split(" to ")
            text_part = parts[0].replace("translate ", "").strip()
            target = parts[1].strip()
            return ("translate", {"text": text_part, "target": target})
        
        if "solve" in text:
            eq = user_input.replace("solve", "").strip()
            return ("math", {"equation": eq})
        
        if "plot" in text:
            expr = user_input.replace("plot", "").strip()
            return ("plot", {"expression": expr})
        
        if "dream" in text:
            prompt = user_input.replace("dream", "").strip()
            return ("dream", {"prompt": prompt})
        
        if "flowchart" in text:
            steps = user_input.replace("flowchart", "").strip()
            return ("flowchart", {"steps": steps})
        
        return (None, None)
    
    def execute(self, task: str, params: dict) -> str:
        if task not in self.agent_map:
            return None
        
        config = self.agent_map[task]
        agent = config["agent"]
        cmd_template = config["cmd"]
        cmd = cmd_template.format(**params)
        
        agent_path = self.agents_path / agent / f"{agent}.py"
        if not agent_path.exists():
            return f"Agent not found: {agent}"
        
        try:
            result = subprocess.run(
                [sys.executable, str(agent_path), cmd],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.agents_path.parent)
            )
            
            output = result.stdout.strip()
            if not output:
                output = result.stderr.strip()
            
            # Clean output - remove header lines
            lines = output.split('\n')
            cleaned = []
            for line in lines:
                if line and not line.startswith('=') and not line.startswith('Commands:') and not line.startswith('Example:') and line != '>':
                    cleaned.append(line)
            
            return '\n'.join(cleaned) if cleaned else "Done"
            
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        print("\n" + "="*50)
        print("CLAWPACK")
        print("="*50)
        print("Commands: translate, solve, plot, dream, flowchart")
        
        while True:
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                if cmd == "/quit":
                    break
                if cmd == "/help":
                    print("translate <text> to <lang> | solve <eq> | plot <expr> | dream <prompt> | flowchart <steps>")
                    continue
                
                task, params = self.route(cmd)
                if task and params:
                    print(f"[{self.agent_map[task]['agent']}] ", end="", flush=True)
                    result = self.execute(task, params)
                    print(result)
                else:
                    print("Command not recognized. Try: translate Hello to Spanish")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    Clawpack().run()
