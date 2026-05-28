"""oral command - Oral argument lookup via CourtListener + Chronicle + Oyez + LLM"""
import requests
from pathlib import Path

name = "/oral"
A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"


def _log(agent, event, detail=""):
    try:
        from agents.webclaw.core.chronicle_ledger import log_event
        log_event(agent=agent, event=event, detail=str(detail)[:500])
    except Exception:
        pass


def get_cl_token():
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"
        for line in env_path.read_text().split("\n"):
            if "COURTLISTENER_TOKEN" in line and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception as e:
        _log("lawclaw", "oral_token_error", e)
    return ""


def llm(prompt, timeout=120):
    try:
        resp = requests.post(
            f"{A2A}/v1/message/llmclaw",
            json={"task": f"/llm {prompt}", "agent": "lawclaw"},
            timeout=timeout,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result and len(result) > 20:
                return result
    except Exception as e:
        _log("lawclaw", "oral_llm_error", str(e)[:100])
    return ""


def chronicle_search(query, limit=10):
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        return results if results else []
    except Exception as e:
        _log("lawclaw", "oral_chronicle_error", str(e)[:100])
    return []


def run(args):
    if not args:
        return (
            "[ORAL] Usage: /oral [case name]\n"
            "  /oral Dobbs\n"
            "  /oral Trump v United States"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"ORAL ARGUMENTS: {args}")
    out.append("=" * 60)

    from agents.lawclaw.commands._memory import show_prior, remember
    prior = show_prior(args, out)

    try:
        cl_context = ""
        audio_urls = []

        # STEP 1: CourtListener docket search + audio lookup
        out.append("")
        out.append("[1/3] Searching CourtListener...")
        token = get_cl_token()

        if not token:
            out.append("  (Add COURTLISTENER_TOKEN to .env)")
        else:
            if " v" not in args.lower() and " v." not in args.lower():
                search_query = f"{args} Supreme Court oral argument"
            else:
                search_query = args

            r = requests.get(
                f"{COURTLISTENER_API}/search/",
                params={
                    "q": search_query,
                    "type": "d",
                    "order_by": "score desc",
                    "page_size": 5,
                    "court": "scotus,ca1,ca2,ca3,ca4,ca5,ca6,ca7,ca8,ca9,ca10,ca11,cadc,cafc",
                },
                headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
                timeout=30,
            )
            if r.status_code != 200:
                out.append(f"  API error: {r.status_code}")
            else:
                dockets = r.json().get("results", [])
                out.append(f"  {len(dockets)} dockets found")
                audio_results = []
                for d in dockets[:5]:
                    docket_id = d.get("docket_id", "") or d.get("id", "")
                    if not docket_id:
                        continue
                    r2 = requests.get(
                        f"{COURTLISTENER_API}/audio/",
                        params={"docket": docket_id, "page_size": 3},
                        headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
                        timeout=30,
                    )
                    if r2.status_code == 200:
                        audio_data = r2.json()
                        audio_results.extend(audio_data.get("results", []))

                if audio_results:
                    out.append(f"  {len(audio_results)} oral arguments found")
                    for a in audio_results[:8]:
                        case_name = a.get("case_name", "Unknown")
                        duration = a.get("duration", "")
                        download_url = a.get("download_url", "") or a.get("local_path_mp3", "")
                        absolute_url = a.get("absolute_url", "")
                        cl_url = f"https://www.courtlistener.com{absolute_url}" if absolute_url else ""

                        duration_str = ""
                        if duration:
                            try:
                                seconds = int(duration)
                                if seconds >= 3600:
                                    duration_str = f"{seconds//3600}h {(seconds%3600)//60}m"
                                elif seconds >= 60:
                                    duration_str = f"{seconds//60}m"
                            except:
                                pass

                        out.append(f"    {case_name}" + (f" ({duration_str})" if duration_str else ""))
                        if download_url:
                            out.append(f"      Audio: {download_url}")
                        if cl_url:
                            out.append(f"      URL: {cl_url}")
                            audio_urls.append(cl_url)
                        out.append("")
                    cl_context = "\n".join(audio_urls)
                else:
                    out.append("  No matching oral arguments in CourtListener")

        # STEP 2: Chronicle index search
        out.append("[2/3] Searching Chronicle...")
        chronicle_results = chronicle_search(f"{args} oral argument supreme court oyez", limit=8)
        chronicle_context = ""
        if chronicle_results:
            parts = []
            for r in chronicle_results[:5]:
                ctx = r["context"] if isinstance(r, dict) else str(r)
                url = r.get("url", "") if isinstance(r, dict) else ""
                parts.append(f"SOURCE: {url}\n{ctx[:1000]}")
            chronicle_context = "\n---\n".join(parts)
            out.append(f"  {len(chronicle_results)} Chronicle references")

        # STEP 3: LLM synthesis with Oyez fallback
        out.append("[3/3] Generating case context...")
        name_slug = args.replace(" ", "+")
        oyez_url = f"https://www.oyez.org/search/{name_slug}"

        if chronicle_context or cl_context:
            prompt = f"""Provide brief context about this case: {args}

CHRONICLE REFERENCES (use these as primary source):
{chronicle_context[:2000] if chronicle_context else "None."}

COURTLISTENER AUDIO:
{cl_context[:1000] if cl_context else "No matching CourtListener audio."}

In 2-3 sentences, explain what the case was about and what was at issue.
Use Chronicle data FIRST. Only reference CourtListener audio if the case names clearly match the query.
If data is limited, say so and point to Oyez for full oral arguments: {oyez_url}
Do not fabricate details.

Context:"""

            result = llm(prompt, timeout=90)
            if result and len(result) > 30:
                out.append("")
                out.append("  [CONTEXT] " + result)

                if audio_urls or chronicle_context:
                    remember(
                        command="/oral",
                        query=args,
                        result_summary=result[:400],
                        source_type="chronicle" if chronicle_context else "web_verified",
                        confidence=0.85,
                        urls=audio_urls[:5] if audio_urls else [oyez_url],
                    )

        out.append("")
        out.append("  Resources (Ctrl+Click):")
        out.append(f"    Oyez Search: {oyez_url}")
        out.append("    Oyez: https://www.oyez.org")
        out.append("    CourtListener Audio: https://www.courtlistener.com/audio/")
        out.append("    Supreme Court: https://www.supremecourt.gov/oral_arguments/")

        return "\n".join(out)

    except Exception as e:
        _log("lawclaw", "oral_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)