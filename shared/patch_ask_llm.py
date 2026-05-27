import sys
path = r"C:\Users\greg\dev\clawpack_v2\shared\base_agent.py"
with open(path, 'r') as f:
    content = f.read()

old_start = '    def ask_llm(self, prompt: str) -> str:\n        """Call LLMClaw with full chronicle context. No truncation, no limits."""'

new_method = '''    def ask_llm(self, prompt: str) -> str:
        """Call Sovereign Gateway directly with Chronicle context. Constitutional path per Article I."""
        try:
            context = ""
            chronicle_results = self.search_chronicle(prompt, limit=10)
            if chronicle_results:
                lines = []
                for c in chronicle_results:
                    if isinstance(c, dict):
                        ctx = c.get("context", "") or c.get("url", "")
                    elif hasattr(c, "context"):
                        ctx = getattr(c, "context", "")
                    else:
                        ctx = str(c)
                    if ctx:
                        lines.append(ctx)
                if lines:
                    context = "\n---\n".join(lines)

            full_prompt = prompt
            if context:
                full_prompt = f"CONTEXT (use this data to answer):\n{context}\n\nQUERY: {prompt}\n\nAnswer the query directly using all relevant data from the context above. Include names, addresses, phone numbers, descriptions, and any other details found in the context."

            from shared.llm.client import get_llm_client
            client = get_llm_client()
            response = client.call_sync(full_prompt, agent=self.name)
            return response.content
        except Exception as e:
            self._log_error("sovereign_gateway", str(e))
        return "Sovereign Gateway unavailable"

    def ask_llm_legacy(self, prompt: str) -> str:
        """DEPRECATED: Call LLMClaw via A2A. Use ask_llm() for direct Sovereign Gateway."""

'''

old_idx = content.find(old_start)
next_method_idx = content.find('\n    def ask_llm_smart', old_idx)

if old_idx != -1 and next_method_idx != -1:
    before = content[:old_idx]
    after = content[next_method_idx:]
    content = before + new_method + after
    with open(path, 'w') as f:
        f.write(content)
    print('DONE: ask_llm now calls Sovereign Gateway directly')
else:
    print(f'MISMATCH: old={old_idx}, next={next_method_idx}')
