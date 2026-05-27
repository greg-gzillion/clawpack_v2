"""federal command - Federal court intelligence hub"""
import requests
import re
from pathlib import Path

name = "/federal"
A2A = "http://127.0.0.1:8766"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v4"

# ── Helpers ──────────────────────────────────────────────────────────────

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
        _log("lawclaw", "federal_get_token_error", e)
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
        _log("lawclaw", "federal_llm_error", e)
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
        _log("lawclaw", "federal_webclaw_error", str(e)[:100])
    return ""


def chronicle_search(query, limit=10):
    """Search Chronicle — the 448MB indexed jurisdiction database."""
    try:
        from agents.webclaw.core.chronicle_ledger import get_chronicle
        c = get_chronicle()
        results = c.recover_by_context(query, limit=limit)
        if results:
            return results  # Return raw results for flexible use
    except Exception as e:
        _log("lawclaw", "federal_chronicle_error", str(e)[:100])
    return []


def cl_get(path, params=None, timeout=15):
    token = get_cl_token()
    if not token:
        return []
    try:
        r = requests.get(
            f"{COURTLISTENER_API}/{path}",
            params=params or {},
            headers={"Authorization": f"Token {token}", "User-Agent": "LawClaw/1.0"},
            timeout=timeout,
        )
        if r.status_code == 200:
            return r.json().get("results", [])
    except Exception as e:
        _log("lawclaw", "federal_cl_error", str(e)[:100])
    return []


def search_jurisdiction_files(query_terms, max_files=10):
    """Search the filesystem jurisdiction tree directly — same pattern as court.py."""
    file_contents = []
    all_urls = []
    try:
        LAW_REFS = Path(__file__).parent.parent.parent.parent / "agents" / "webclaw" / "references" / "lawclaw"
        juris_base = LAW_REFS / "jurisdictions" / "us"
        
        if juris_base.exists():
            for md_file in sorted(juris_base.rglob("*.md")):
                try:
                    content = md_file.read_text(encoding='utf-8', errors='ignore')
                    if any(t.lower() in content.lower() for t in query_terms if len(t) > 2):
                        rel = md_file.relative_to(LAW_REFS)
                        file_contents.append((str(rel), content[:2000]))
                        urls = re.findall(r'https?://[^\s\)\]\<\>\"]+', content)
                        all_urls.extend(urls)
                        if len(file_contents) >= max_files:
                            break
                except:
                    pass
    except Exception as e:
        _log("lawclaw", "federal_filesystem_error", str(e)[:100])
    
    return file_contents, all_urls


# ── Main ─────────────────────────────────────────────────────────────────

def run(args):
    if not args:
        return (
            "[FEDERAL] Usage: /federal [circuit|district|supreme|city|state|rules|pacer|judges|opinions]\n"
            "  /federal 9th circuit        — all districts in circuit\n"
            "  /federal NY                 — federal districts in a state\n"
            "  /federal SDNY               — district info + PACER\n"
            "  /federal SDNY judges        — judge roster\n"
            "  /federal SDNY opinions      — recent opinions (CourtListener)\n"
            "  /federal SDNY local rules   — local rules link\n"
            "  /federal Bedford VA         — nearest federal courthouse\n"
            "  /federal supreme            — SCOTUS opinions\n"
            "  /federal frcp 12            — Federal Rules\n"
            "  /federal pacer              — fee schedule"
        )

    out = []
    out.append("")
    out.append("=" * 60)
    out.append(f"FEDERAL COURTS: {args}")
    out.append("=" * 60)
    out.append("")
    out.append("  Tip: Hold Ctrl+Click on any URL to open it in your browser.")

    try:
        al = args.lower().strip()

        # ── CHRONICLE-FIRST: Search the index for EVERY query ────────────
        chronicle_results = chronicle_search(f"{args} federal court district circuit judge", limit=10)
        
        # Build context from Chronicle hits
        chronicle_context = ""
        chronicle_urls = []
        if chronicle_results:
            parts = []
            for r in chronicle_results[:8]:
                ctx = r["context"] if isinstance(r, dict) else str(r)
                url = r.get("url", "") if isinstance(r, dict) else ""
                if url:
                    chronicle_urls.append(url)
                parts.append(f"SOURCE: {url}\n{ctx[:1200]}")
            chronicle_context = "\n\n---\n\n".join(parts)

        # ── FILESYSTEM: Search jurisdiction files for matching content ──
        query_terms = [t for t in al.split() if len(t) > 1]
        filesystem_files, filesystem_urls = search_jurisdiction_files(query_terms, max_files=8)
        
        filesystem_context = ""
        if filesystem_files:
            parts = []
            for path, content in filesystem_files:
                parts.append(f"--- {path} ---\n{content}")
            filesystem_context = "\n\n".join(parts)

        # ── SUPREME COURT ────────────────────────────────────────────────
        if "supreme" in al or "scotus" in al:
            out.append("  Supreme Court of the United States")
            out.append("  Website: https://www.supremecourt.gov")
            out.append("")
            ops = cl_get("opinions/", {"court": "scotus", "order_by": "-date_filed", "page_size": 8})
            if ops:
                out.append(f"  Recent opinions via CourtListener ({len(ops)}):")
                for o in ops:
                    date = o.get("date_filed", "?") or "?"
                    case = o.get("case_name", "Unknown")
                    url = f"https://www.courtlistener.com{o.get('absolute_url', '')}"
                    out.append(f"    {date} | {case}")
                    out.append(f"    {url}")
            else:
                out.append("  (Live opinions unavailable — see https://www.oyez.org)")
            out.append("")
            out.append("  Resources (Ctrl+Click):")
            out.append("    https://www.supremecourt.gov")
            out.append("    https://www.oyez.org")
            return "\n".join(out)

        # ── PACER ────────────────────────────────────────────────────────
        if al == "pacer":
            out.append("  PACER — Public Access to Court Electronic Records")
            out.append("")
            out.append("  Registration: https://pacer.uscourts.gov/register-account")
            out.append("  Fees: $0.10/page ($3.00 max per document)")
            out.append("  Waived: under $30/quarter automatically waived")
            out.append("  Free:  https://www.courtlistener.com (RECAP archive)")
            out.append("")
            out.append("  /federal [district]  — e.g. /federal SDNY for PACER link")
            out.append("  /docket [case number] — search for a specific case")
            return "\n".join(out)

        # ── FEDERAL RULES ────────────────────────────────────────────────
        if any(kw in al for kw in ["rule", "frcp", "fre", "frap"]):
            out.append("  Federal Rules Reference")
            out.append("")
            rule_num = re.search(r'\b(\d+)\b', args)
            rule_type = "frcp"
            if "fre" in al or "evidence" in al:
                rule_type = "fre"
            elif "frap" in al or "appellate" in al:
                rule_type = "frap"
            if rule_num:
                rule_url = f"https://www.law.cornell.edu/rules/{rule_type}/rule_{rule_num.group(1)}"
                out.append(f"  {rule_type.upper()} Rule {rule_num.group(1)}: {rule_url}")
                html = webclaw_fetch(rule_url)
                if html and len(html) > 100:
                    summary = llm(
                        f"Summarize {rule_type.upper()} Rule {rule_num.group(1)} from this page. "
                        f"Be concise. Quote key language (under 15 words per quote).\n\n{html[:3000]}",
                        timeout=60,
                    )
                    if summary:
                        out.append("")
                        out.append(summary)
            else:
                out.append("  FRCP: https://www.law.cornell.edu/rules/frcp")
                out.append("  FRE:  https://www.law.cornell.edu/rules/fre")
                out.append("  FRAP: https://www.law.cornell.edu/rules/frap")
                out.append("  Tip:  /federal frcp 12  — text of FRCP Rule 12")
            return "\n".join(out)

        # ── CORE: Chronicle + Filesystem + LLM synthesis ─────────────────
        # Combine all data sources
        all_context = ""
        if filesystem_context:
            all_context += f"JURISDICTION FILES:\n{filesystem_context[:3000]}\n\n"
        if chronicle_context:
            all_context += f"CHRONICLE INDEX:\n{chronicle_context[:3000]}"
        
        all_urls = list(set(filesystem_urls + chronicle_urls))

        if all_context.strip():
            out.append("")
            out.append(f"  Sources: Chronicle + {len(filesystem_files)} jurisdiction files")
            
            # Let the LLM synthesize from real data
            prompt = f"""Answer this federal court query using ONLY the data below: {args}

{all_context[:4000]}

Provide: court name, address, phone, website URL, jurisdiction, and how to access records.
If the data contains federal district information, include it with PACER links.
If the data doesn't answer the query, say exactly what's missing.
Be specific. Cite sources. Include URLs.

Answer:"""
            
            result = llm(prompt, timeout=90)
            if result and len(result) > 50:
                out.append("")
                out.append("=" * 60)
                out.append(result)
                out.append("=" * 60)
            else:
                # LLM failed — show raw filesystem data
                out.append("")
                out.append("=" * 60)
                out.append("[RAW DATA FROM JURISDICTION FILES]")
                out.append(all_context[:3000])
                out.append("=" * 60)
        else:
            out.append("")
            out.append("  No data found in Chronicle or jurisdiction files.")
            out.append("  Try: /federal supreme, /federal pacer, /federal frcp 12")

        # ── Show URLs ────────────────────────────────────────────────────
        if all_urls:
            gov_urls = sorted(set(u for u in all_urls if '.gov' in u.lower()))
            other_urls = sorted(set(u for u in all_urls if '.gov' not in u.lower()))
            ranked = gov_urls + other_urls
            if ranked:
                out.append("")
                out.append("  Relevant URLs (Ctrl+Click):")
                for url in ranked[:15]:
                    out.append(f"    {url}")

        out.append("")
        out.append("  Federal Resources (Ctrl+Click):")
        out.append("    https://www.supremecourt.gov")
        out.append("    https://pacer.uscourts.gov")
        out.append("    https://www.uscourts.gov")
        out.append("    https://www.courtlistener.com")
        return "\n".join(out)

    except Exception as e:
        _log("lawclaw", "federal_run_error", str(e)[:300])
        out.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(out)