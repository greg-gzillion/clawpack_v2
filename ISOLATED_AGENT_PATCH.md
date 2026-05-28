"""
mathematicaclaw agent_handler.py — PATCH to connect to shared infrastructure.

BEFORE: own_llm=True, call_agent=False, chronicle=False
AFTER:  uses BaseAgent.ask_llm(), call_agent(), search_chronicle()

Apply by replacing the ask_llm calls and adding cross-agent delegation.
This is the pattern for ALL isolated agents (drawclaw, fileclaw, etc.)
"""

# ── HOW TO PATCH ANY ISOLATED AGENT ──────────────────────────────────────────
#
# Step 1: Find where the agent calls its own LLM function.
#         Look for: requests.post(...llmclaw...) or openai.chat() or similar
#
# Step 2: Replace with self.ask_llm() or self.smart_ask()
#
# Step 3: Add cross-agent calls where useful
#
# Step 4: Use self.search_chronicle() before external API calls
#
# The diff for mathematicaclaw looks like this:
# ─────────────────────────────────────────────────────────────────────────────

BEFORE = """
# In mathematicaclaw/agent_handler.py — current broken pattern:

class MathematicaClawHandler(BaseAgent):
    def handle(self, task: str) -> dict:
        self.track_interaction()
        try:
            # OWN LLM CALL — bypasses Sovereign Gateway
            import requests
            resp = requests.post(
                "http://127.0.0.1:8766/v1/message/llmclaw",
                json={"task": f"/llm {task}", "agent": "mathematicaclaw"},
                timeout=120
            )
            result = resp.json().get("result", "")
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "result": str(e)}
"""

AFTER = """
# In mathematicaclaw/agent_handler.py — connected pattern:

from shared._agent_helpers import llm, smart, chronicle_text, delegate, log_err

class MathematicaClawHandler(BaseAgent):
    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        try:
            # Search Chronicle first — may already have the answer
            ctx = self.search_chronicle(task, limit=5)
            context_str = ""
            if ctx:
                context_str = "\\n".join(
                    r.get("context", "")[:500] if isinstance(r, dict) else str(r)
                    for r in ctx[:3]
                )

            # Use BaseAgent.ask_llm() — Chronicle-enriched, budget-tracked
            prompt = f"Solve or explain this mathematical problem:\\n{task}"
            if context_str:
                prompt += f"\\n\\nRelevant context:\\n{context_str}"

            result = self.ask_llm(prompt)

            # Cross-agent: offer visualization for data results
            if any(kw in task.lower() for kw in ["plot", "graph", "chart", "visualize"]):
                chart = self.call_agent("plotclaw", f"/plot {task}", timeout=30)
                if chart:
                    result += f"\\n\\nVisualization: {chart}"

            # Cross-agent: offer document export for complex solutions
            if len(result) > 500:
                result += "\\n\\nUse /export to save this as a document via docuclaw."

            return {"status": "success", "result": result}
        except Exception as e:
            self._log_error("handle_error", str(e)[:200])
            return {"status": "error", "result": str(e)}
"""

# ── SAME PATTERN FOR drawclaw ─────────────────────────────────────────────────

DRAWCLAW_ADDITIONS = """
# drawclaw currently has call_agent=False, own_llm=True
# Add these to drawclaw/agent_handler.py handle() method:

# Before LLM call — search Chronicle for style references
style_refs = self.search_chronicle(task, limit=3)

# Use BaseAgent.ask_llm() instead of own implementation
result = self.ask_llm(f"Create drawing instructions for: {task}")

# Cross-agent: send result to docuclaw if export requested
if "export" in task.lower() or "save" in task.lower():
    doc = self.call_agent("docuclaw", f"/create {result}", timeout=60)
    if doc:
        result += f"\\n\\nExported: {doc}"
"""

FILECLAW_ADDITIONS = """
# fileclaw currently has call_agent=False, own_llm=False
# It handles 52 file formats but is completely isolated
# Add these capabilities:

# Cross-agent: when analyzing a legal document, route to lawclaw
if any(ext in task for ext in [".pdf", ".docx"]) and "legal" in task.lower():
    analysis = self.call_agent("lawclaw", f"/analyze {task}", timeout=60)

# Cross-agent: when creating output documents, route to docuclaw
if "create" in task.lower() or "export" in task.lower():
    doc = self.call_agent("docuclaw", f"/create {task}", timeout=60)

# Chronicle: record processed file references
self.record_in_chronicle(
    url=f"file://{task}",
    context=f"File processed by fileclaw: {task}",
    source="fileclaw"
)
"""

# ── HOW TO APPLY TO ALL 21 AGENTS IN ONE SESSION ────────────────────────────
#
# Priority 1 (isolated, fix now):
#   drawclaw, fileclaw, mathematicaclaw
#
# Priority 2 (has own LLM, fix next):
#   claw_coder, crustyclaw, designclaw, docuclaw, draftclaw
#   flowclaw, interpretclaw, langclaw, liberateclaw, mediclaw
#
# Priority 3 (already connected, leave alone):
#   lawclaw, dataclaw, dreamclaw, langclaw, llmclaw
#   plotclaw, rustypycraw, txclaw, webclaw
#
# The fix for each:
# 1. Find own LLM call → replace with self.ask_llm()
# 2. Add self.search_chronicle() before expensive operations
# 3. Add self.call_agent() for natural cross-agent flows
# 4. Replace except: pass with self._log_error()
# That's 4 changes per agent. ~30 minutes per agent. One session for all 9.
