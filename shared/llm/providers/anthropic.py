import aiohttp
async def call_anthropic(provider, prompt, max_tokens, temp):
    async with aiohttp.ClientSession() as s:
        h = {"x-api-key": provider["key"], "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
        d = {"model": provider["model"], "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": temp}
        async with s.post(f"{provider["base_url"]}/messages", headers=h, json=d, timeout=aiohttp.ClientTimeout(total=120)) as r:
            j = await r.json()
            if "error" in j: raise Exception(f"Anthropic: {j["error"]}")
            return {"content": j["content"][0]["text"], "tokens": j.get("usage", {}).get("input_tokens", 0) + j.get("usage", {}).get("output_tokens", 0), "cost": 0.015}
