"""logo command - Constitutional design generation with memory + enrichment"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
name = "logo"

def run(args: str, agent=None) -> str:
    from agents.designclaw.commands._memory import recall, remember
    from agents.designclaw.commands._helpers import save_html
    
    query = args.strip()
    if not query:
        return "Usage: /brand|/logo|/colors|/kit|/html <description>"
    
    # Check memory for prior designs
    prior = recall(query, limit=2)
    prior_text = ""
    if prior:
        prior_text = "\n".join(f"Prior design: {p.get('fact','')[:200]}" for p in prior)
    
    # Detect command type from query prefix
    cmd_type = query.split()[0].lower() if query else "brand"
    
    prompts = {
        "brand": f"Create a complete brand identity: 1. Brand essence 2. Logo concept 3. Color palette with hex codes 4. Typography 5. Brand voice.\n\nBrief: {query}",
        "colors": f"Create a color palette with 5 hex codes and usage notes.\n\nContext: {query}",
        "mood": f"Describe an aesthetic mood direction: vibe, color story, texture, typography style, references.\n\nContext: {query}",
        "typography": f"Recommend font pairings with Google Fonts links, header and body.\n\nStyle: {query}",
        "copy": f"Write brand copy: tagline, value proposition, mission, 3 brand voice adjectives.\n\nBrand: {query}",
        "logo": f"Create an SVG logo design with shapes, colors, layout. Include SVG code.\n\nLogo for: {query}",
        "kit": f"Create a complete brand kit as HTML with inline CSS: brand name, logo concept, color swatches, typography, brand voice, sample business card.\n\nBrand: {query}\n\nReturn complete HTML.",
        "html": f"Create a complete responsive HTML page with embedded CSS. Beautiful and modern.\n\nDesign for: {query}\n\nReturn complete HTML.",
    }
    
    prompt = prompts.get(cmd_type, f"Senior design consultant. Answer concisely: {query}")
    if prior_text:
        prompt = f"Prior designs for reference:\n{prior_text}\n\n{prompt}"
    
    if agent and hasattr(agent, 'ask_llm'):
        result = agent.ask_llm(prompt)
    else:
        return "Error: No agent context"
    
    # Save HTML for kit/html commands
    if cmd_type in ("kit", "html"):
        fn = save_html(result, query.replace(" ", "_")[:40])
        result = f"Saved: {fn}\n\n{result}"
    
    remember(command=cmd_type, query=query, result_summary=result[:400],
             source_type="chronicle", confidence=0.85,
             metadata={"type": cmd_type})
    return result
