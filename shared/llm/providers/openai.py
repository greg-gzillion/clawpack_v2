import aiohttp
async def call_openai(provider, prompt, max_tokens, temp):
    async with aiohttp.ClientSession() as s:
        h = {"Authorization": f"Bearer {provider["key"]}", "Content-Type": "application/json"}
        d = {"model": provider["model"], "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": temp}
        async with s.post(f"{provider["base_url"]}/chat/completions", headers=h, json=d, timeout=aiohttp.ClientTimeout(total=120)) as r:
            j = await r.json()
            if "error" in j: raise Exception(f"OpenAI: {j["error"]}")
            return {"content": j["choices"][0]["message"]["content"], "tokens": j.get("usage", {}).get("total_tokens", 0), "cost": 0.01}
