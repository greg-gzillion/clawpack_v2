import aiohttp
async def call_ollama(provider, prompt, max_tokens, temp, model):
    m = model if model and model != "governance" else provider.get("model", "llama3.2:3b")
    async with aiohttp.ClientSession() as s:
        d = {"model": m, "prompt": prompt, "stream": False, "options": {"num_predict": max_tokens, "temperature": temp}}
        async with s.post(f"{provider["base_url"]}/api/generate", json=d, timeout=aiohttp.ClientTimeout(total=600)) as r:
            j = await r.json()
            return {"content": j.get("response", ""), "tokens": j.get("eval_count", 0), "cost": 0.0}
