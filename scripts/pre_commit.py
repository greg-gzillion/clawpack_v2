#!/usr/bin/env python3
"""Constitutional Pre-Commit Hook — Blocks forbidden imports and exposed secrets.

   Install: python scripts/install_hooks.py
   This file is TRACKED in git. Run install_hooks.py to deploy to .git/hooks/
"""
import sys, re, subprocess
from pathlib import Path

FORBIDDEN = [
    (r"import\s+ollama", "import ollama"),
    (r"from\s+ollama\s+import", "from ollama import"),
    (r"from\s+groq\s+import", "from groq import"),
    (r"import\s+anthropic", "import anthropic"),
    (r"openrouter\.ai", "openrouter.ai URL"),
    (r"api\.groq\.com", "api.groq.com URL"),
    (r"localhost:11434(?!/api/tags)", "localhost:11434 direct Ollama"),
    (r"subprocess\.run\(\s*\[\s*[\"']ollama[\"']\s*,\s*[\"']run[\"']", "subprocess ollama run"),
    (r"from\s+core\.llm_manager\s+import", "deprecated core.llm_manager"),
    (r"from\s+core\.llm\.manager\s+import", "deprecated core.llm.manager"),
    (r"requests\.post\(\s*[\"'].*chat/completions", "direct chat/completions POST"),
]

SECRETS = [
    (r"gsk_[A-Za-z0-9]{30,}", "Groq API key"),
    (r"sk-[A-Za-z0-9]{30,}", "OpenAI API key"),
    (r"sk-ant-[A-Za-z0-9]{30,}", "Anthropic API key"),
    (r"sk-or-[A-Za-z0-9]{30,}", "OpenRouter API key"),
]

EXEMPT = ["shared/llm/", "_archive/", "__pycache__/", ".git/"]

def get_staged():
    result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                          capture_output=True, text=True)
    return [f for f in result.stdout.strip().split('\n') if f.endswith('.py') and f.strip()]

violations = []
for f in get_staged():
    if any(e in f for e in EXEMPT): continue
    try:
        content = Path(f).read_text(encoding='utf-8', errors='ignore')
        for pattern, msg in FORBIDDEN:
            if re.search(pattern, content):
                violations.append(f"{f}: {msg}")
        for pattern, msg in SECRETS:
            if re.search(pattern, content):
                violations.append(f"SECRET EXPOSED in {f}: {msg}")
    except: pass

if violations:
    print("CONSTITUTIONAL VIOLATIONS DETECTED:")
    for v in violations: print(f"  {v}")
    print("\nCommit BLOCKED. Fix violations before committing.")
    sys.exit(1)
print("Constitutional check passed")
