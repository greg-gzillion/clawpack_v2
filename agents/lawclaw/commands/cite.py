"""cite command - Parse and validate law citations with WebClaw intelligence"""
import re

name = "/cite"

from agents.lawclaw.commands._helpers import llm, webclaw, chronicle, delegate
from agents.lawclaw.commands._memory import show_prior, remember

# Concept router: maps citation patterns to the correct legal domain
CONCEPT_MAP = {
    # Constitutional Law
    "amendment": "constitutional law fourth fifth first amendment",
    "constitution": "constitutional law supreme court landmark",
    # Criminal Procedure
    "miranda": "criminal procedure fifth sixth amendment miranda",
    "terry": "criminal procedure fourth amendment stop frisk",
    "mapp": "criminal procedure fourth amendment exclusionary rule",
    "gideon": "criminal procedure sixth amendment right counsel",
    # UCC Articles
    "ucc 1-": "ucc uniform commercial code article 1 general provisions",
    "ucc 2-": "contract law ucc article 2 sales commercial",
    "ucc 2a": "ucc article 2a leases",
    "ucc 3-": "ucc article 3 negotiable instruments banking",
    "ucc 4-": "ucc article 4 bank deposits banking finance",
    "ucc 4a": "ucc article 4a funds transfers banking",
    "ucc 5-": "ucc article 5 letters credit banking",
    "ucc 7-": "ucc article 7 documents title",
    "ucc 8-": "ucc article 8 investment securities",
    "ucc 9-": "ucc article 9 secured transactions business",
    # Federal Rules
    "frcp": "federal rules civil procedure frcp",
    "frep": "federal rules evidence fre",
    "frcrp": "federal rules criminal procedure",
    "frbp": "federal rules bankruptcy procedure",
    "frap": "federal rules appellate procedure",
    # USC Titles
    "42 usc 1983": "civil rights section 1983 constitutional law",
    "11 usc": "bankruptcy code title 11",
    "18 usc": "criminal law federal crimes title 18",
    "26 usc": "tax law internal revenue code",
    "28 usc": "federal courts judiciary title 28",
    "29 usc": "labor law employment title 29",
    "35 usc": "patent intellectual property title 35",
    "15 usc": "commerce trade antitrust title 15",
    # Case Law
    "roe v wade": "constitutional law fourteenth amendment due process abortion",
    "brown v board": "constitutional law fourteenth amendment equal protection civil rights",
    "marbury v madison": "constitutional law separation powers judicial review supreme court",
    "chevron": "administrative law agency deference judicial review",
    "citizens united": "constitutional law first amendment campaign finance corporate speech",
    "katz v": "constitutional law fourth amendment criminal procedure privacy",
    "carpenter v": "constitutional law fourth amendment technology cell phone",
    "gideon v": "constitutional law sixth amendment criminal procedure right counsel",
    "mcdonald v": "constitutional law second amendment fourteenth incorporation",
    "dobbs v": "constitutional law fourteenth amendment due process abortion",
    "obergefell v": "constitutional law fourteenth amendment equal protection marriage",
    "loving v": "constitutional law fourteenth amendment equal protection marriage",
    "lawrence v": "constitutional law fourteenth amendment due process privacy",
    "heller": "constitutional law second amendment right bear arms",
    "brandenburg": "constitutional law first amendment free speech incitement",
    "new york times v sullivan": "constitutional law first amendment defamation press",
    "gibbons v": "constitutional law commerce clause federalism",
    "wickard v": "constitutional law commerce clause substantial effects",
    "lopez": "constitutional law commerce clause limits",
    "youngstown": "constitutional law separation powers executive authority",
    "nixon": "constitutional law executive privilege separation powers",
}


def route_concept(query):
    """Map a citation query to the correct legal domain for Chronicle search."""
    query_lower = query.lower().strip()
    for key in sorted(CONCEPT_MAP.keys(), key=len, reverse=True):
        if key in query_lower:
            return CONCEPT_MAP[key]
    return None


def run(args, agent=None):
    if not args:
        return "[CITE] Usage: /cite [citation] -- e.g., /cite 42 USC 1983, /cite Roe v. Wade, /cite 410 U.S. 113"

    output = []
    output.append("")
    output.append("=" * 60)
    output.append(f"CITATION: {args}")
    output.append("=" * 60)

    prior = show_prior(args, output)

    try:
        # STEP 0: Route to correct legal domain
        domain = route_concept(args)
        if domain:
            search_query = f"{args} {domain}"
            output.append("")
            output.append(f"  Routed to: {domain}")
        else:
            search_query = f"{args} citation statute case law"

        # STEP 1: Search Chronicle for citation references
        output.append("")
        output.append("[1/3] Searching Chronicle...")
        chronicle_context = ""
        try:
            from agents.webclaw.core.chronicle_ledger import get_chronicle
            chronicle = get_chronicle()
            results = chronicle.recover_by_context(search_query, limit=10)
            if results:
                lines = []
                for r in results[:5]:
                    ctx = r["context"] if isinstance(r, dict) else str(r)
                    url = r["url"] if isinstance(r, dict) else ""
                    lines.append(f"SOURCE: {url}\n{ctx[:1000]}")
                chronicle_context = "\n\n---\n\n".join(lines)
                output.append(f"  Found {len(results)} related references")
            else:
                output.append("  No local references found")
        except Exception as e:
            output.append(f"  Chronicle error: {e}")

        # STEP 2: Fetch live URLs via WebClaw
        output.append("[2/3] Fetching live sources via WebClaw...")
        urls_found = re.findall(r'https?://[^\s\)\]\<\>\"]+', args + " " + chronicle_context)
        web_context = ""
        for url in urls_found[:3]:
            try:
                resp = requests.post(
                    f"{A2A}/v1/message/webclaw",
                    json={"task": f"fetch {url}", "agent": "lawclaw"},
                    timeout=15
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data.get("result", "")
                    if content and "fetch failed" not in content.lower():
                        web_context += f"\n\nSOURCE: {url}\n{content[:800]}"
                        output.append(f"  Fetched: {url[:60]}...")
            except:
                pass
        if not web_context:
            output.append("  No live URLs fetched")

        # STEP 3: Parse and explain citation via LLM with retry and fallback
        output.append("[3/3] Parsing citation via LLM...")
        prompt = f"""Parse and fully explain this legal citation: {args}

CHRONICLE REFERENCES:
{chronicle_context if chronicle_context else "No indexed references found."}

LIVE WEB DATA:
{web_context if web_context else "No live web data fetched."}

Provide:
1. CITATION TYPE - Is this a statute, case, regulation, or other?
2. FULL TITLE - The complete name and official title
3. JURISDICTION - Federal, state, or other; which court or legislature
4. SUBSTANCE - What the statute says or what the case held
5. AUTHORITY - Binding vs persuasive; current status (good law/overruled/modified)
6. RELATED CITATIONS - Key related statutes, cases, or regulations
7. WHERE TO FIND - Official sources and free access points
8. PRACTICAL NOTES - How it's used, key elements, common issues

Cite your sources. If you don't know, say so rather than guessing.

Citation Analysis:"""

        result = ""
        for attempt in range(2):
            resp = requests.post(
                f"{A2A}/v1/message/llmclaw",
                json={"task": f"/llm {prompt}", "agent": "lawclaw"},
                timeout=180
            )
            if resp.status_code == 200:
                result = resp.json().get("result", "")
                if result and len(result) > 50:
                    output.append("")
                    output.append("=" * 60)
                    output.append(result)
                    output.append("=" * 60)
                    
                    # Write to shared memory
                    remember(
                        command="/cite",
                        query=args[:200],
                        result_summary=result[:400],
                        source_type="web_verified" if web_context else "chronicle",
                        confidence=0.85 if web_context else 0.80,
                    )
                    
                    return "\n".join(output)

        # LLM failed — fall back to WebClaw AI analysis
        output.append("  LLM unavailable, using WebClaw intelligence...")
        fallback_content = web_context if web_context else chronicle_context
        if fallback_content:
            resp = requests.post(
                f"{A2A}/v1/message/webclaw",
                json={"task": f"search {args} citation legal analysis", "agent": "lawclaw"},
                timeout=60
            )
            if resp.status_code == 200:
                result = resp.json().get("result", "")
                if result and len(result) > 50:
                    output.append("")
                    output.append("=" * 60)
                    output.append("[WEBCLAW ANALYSIS]")
                    output.append(result)
                    output.append("=" * 60)
                    
                    # Write to shared memory
                    remember(
                        command="/cite",
                        query=args[:200],
                        result_summary=result[:400],
                        source_type="web_verified",
                        confidence=0.80,
                    )
                    
                    return "\n".join(output)

        output.append("[ERROR] Unable to retrieve citation information")
        return "\n".join(output)

    except Exception as e:
        output.append(f"\n[ERROR] {str(e)[:300]}")
        return "\n".join(output)