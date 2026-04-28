# DesignClaw

AI-powered design assistant for brand identity, color palettes, typography, mood boards, and HTML generation.

## Commands

| Command | Description |
|---------|-------------|
| `/brand <brief>` | Complete brand identity (essence, logo, colors, type, voice) |
| `/colors <context>` | Color palette with hex codes and usage notes |
| `/mood <aesthetic>` | Mood board direction (vibe, colors, texture, references) |
| `/type <style>` | Typography recommendations with Google Fonts |
| `/copy <brand>` | Copywriting (tagline, voice, mission) |
| `/logo <brief>` | SVG logo design concept |
| `/kit <brand>` | Full brand kit as responsive HTML page |
| `/html <design>` | Complete responsive HTML page with embedded CSS |
| `/help` | Show commands |
| `/stats` | Show interaction statistics |

## Quick Start
/brand eco-friendly fashion startup
/colors luxury spa
/kit modern coffee shop
/html landing page for SaaS product

text

## File Structure
agents/designclaw/
├── agent_handler.py # A2A handler
├── core/
│ └── agent.py # Design engine
├── commands/
│ └── logo.py # Logo generation
├── exports/ # Generated designs
└── providers/ # External services

text

## A2A Integration

```python
self.call_agent("designclaw", "/brand sustainable fashion brand")
self.call_agent("designclaw", "/kit modern coffee shop")
Output
HTML files saved to exports/ with preview

Brand kits include color swatches, typography, business cards

Landing pages are responsive with modern CSS