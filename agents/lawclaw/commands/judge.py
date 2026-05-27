"""judge command - Federal judge lookup via FJC + Chronicle + CourtListener"""
import requests
from pathlib import Path

name = "/judge"
A2A = "http://127.0.0.1:8766"


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
        _log("lawclaw", "judge_token_error", e)
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
        _log("lawclaw", "judge_llm_error", e)
    return ""


def webclaw_fetch(url):
    try:
        resp = requests.post(
            f"{A2A}/v1/message/webclaw",
            json={"task": f"fetch {url}", "agent": "lawclaw"},
            timeout=20,
        )
        if resp.status_code == 200:
            result = resp.json().get("result", "")
            if result and len(result) > 50:
                return result
    except Exception as e:
        _log("lawclaw", "judge_webclaw_error", str(e)[:100])
    return ""


def chronicle_search(query, limit=10):
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        return results if results else []
    except Exception as e:
        _log("lawclaw", "judge_chronicle_error", str(e)[:100])
    return []


def cl_get(path, params=None, timeout=15):
    token = get_cl_token()
    if not token:
        return []
    try:
        r = requests.get(
            f"https://www.courtlistener.com/api/rest/v4/{path}",
            params=params or {},
            headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.json().get("results", [])
    except Exception as e:
        _log("lawclaw", "judge_cl_error", str(e)[:100])
    return []


def run(args):
    if not args:
        return "[JUDGE] Usage: /judge [judge name] -- e.g., /judge Sotomayor, /judge Robert Pitman"

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"JUDGE: {args}")
    out.append("=" * 60)

    try:
        name_slug = args.lower().strip().replace(" ", "-").replace(".", "")
        parts = args.strip().split()
        last_name = parts[-1] if len(parts) >= 2 else args

        # STEP 1: Chronicle
        out.append("")
        out.append("[1/3] Searching Chronicle...")
        chronicle_results = chronicle_search(f"{args} judge federal court supreme", limit=8)
        chronicle_context = ""
        if chronicle_results:
            parts_ctx = []
            for r in chronicle_results[:5]:
                ctx = r["context"] if isinstance(r, dict) else str(r)
                url = r.get("url", "") if isinstance(r, dict) else ""
                parts_ctx.append(f"SOURCE: {url}\n{ctx[:1200]}")
            chronicle_context = "\n\n---\n\n".join(parts_ctx)
            out.append(f"  Found {len(chronicle_results)} Chronicle references")

        # STEP 2: FJC
        out.append("[2/3] Fetching FJC biography...")
        fjc_url = f"https://www.fjc.gov/history/judges/{name_slug}"
        fjc_html = webclaw_fetch(fjc_url)
        fjc_context = ""

        if fjc_html and len(fjc_html) > 200:
            fjc_context = f"FJC SOURCE: {fjc_url}\n{fjc_html[:3000]}"
            out.append("  FJC biography retrieved")
        else:
            search_url = f"https://www.fjc.gov/history/judges/search?q={args.replace(' ', '%20')}"
            out.append(f"  Direct FJC lookup failed. Search: {search_url}")

        # STEP 3: CourtListener (search by last name for better coverage)
        out.append("[3/3] Checking CourtListener...")
        people = cl_get("people/", {"name__icontains": last_name, "page_size": 10})
        # Filter to exact name match if multiple results
        if len(parts) >= 2 and len(people) > 1:
            people = [p for p in people if all(
                pt.lower() in f"{p.get('name_first', '')} {p.get('name_last', '')}".lower()
                for pt in parts
            )]
        cl_context = ""
        if people:
            out.append(f"  Found {len(people)} CourtListener records")
            parts_cl = []
            for p in people[:5]:
                first = p.get("name_first", "") or ""
                last = p.get("name_last", "") or ""
                positions = p.get("positions", [])
                pos_lines = []
                for pos in positions[:3]:
                    court = pos.get("court", {})
                    court_name = court.get("full_name", "") if isinstance(court, dict) else ""
                    pos_type = pos.get("position_type", "") or ""
                    date_start = pos.get("date_start", "") or ""
                    date_term = pos.get("date_termination", "") or ""
                    if court_name:
                        status = f"{date_start} to {date_term}" if date_term else f"since {date_start}"
                        pos_lines.append(f"{pos_type}: {court_name} ({status})")
                fjc_id = p.get("fjc_id", "") or ""
                if fjc_id:
                    pos_lines.append(f"FJC ID: {fjc_id} | https://www.fjc.gov/node/{fjc_id}")
                parts_cl.append(f"{first} {last}\n" + "\n".join(pos_lines))
            cl_context = "\n\n".join(parts_cl)
        else:
            out.append("  No CourtListener records found")

        # STEP 4: LLM synthesis
        all_context = ""
        if chronicle_context:
            all_context += f"CHRONICLE:\n{chronicle_context[:1500]}\n\n"
        if fjc_context:
            all_context += f"FJC BIOGRAPHY:\n{fjc_context[:2000]}\n\n"
        if cl_context:
            all_context += f"COURTLISTENER:\n{cl_context[:1000]}\n\n"

        if all_context.strip():
            out.append("")
            out.append("[SYNTHESIS] Generating biography...")

            prompt = f"""Write a concise biography of {args} in 3-4 sentences. 
Each sentence must contain new information not already stated.
Do not repeat any fact. Do not use bullet points.
Only mention specific cases if they appear explicitly in the source data provided.
Do not infer or guess case involvement from names or context.

Sources:
FJC: {fjc_context[:2000]}
Chronicle: {chronicle_context[:1000]}
CourtListener: {cl_context[:500] if cl_context else "No CourtListener data found."}

Biography:"""

            result = llm(prompt, timeout=90)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)
        else:
            out.append("")
            out.append("  No data found from any source.")
            out.append(f"  Try FJC directly: {fjc_url}")

        # URLs
        out.append("")
        out.append("  Resources (Ctrl+Click):")
        out.append(f"    FJC Biography: {fjc_url}")
        out.append("    FJC Judge Directory: https://www.fjc.gov/history/judges")
        out.append("    CourtListener: https://www.courtlistener.com")

        return "\n".join(out)

    except Exception as e:
        _log("lawclaw", "judge_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)