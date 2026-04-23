import sys
from pathlib import Path
LLMCLAW_DIR = Path(__file__).parent.parent / 'llmclaw'
sys.path.insert(0, str(LLMCLAW_DIR))
from commands.llm_enhanced import run as llm_run

def process_task(task, agent=None):
    task = task.strip()
    if task.startswith('/ask'):
        task = task[5:].strip()
    try:
        result = llm_run(task)
        return {'status': 'success', 'result': result}
    except Exception as e:
        return {'status': 'error', 'result': str(e)}
