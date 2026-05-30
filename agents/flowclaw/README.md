# FlowClaw v5 — Constitutional Diagram & Flowchart Agent

## What It Does
Generates diagrams, flowcharts, sequences, architecture diagrams, and mindmaps
using Mermaid.js syntax. Outputs to browser, exports to multiple formats.

## Commands

| Command | Description |
|---------|-------------|
| `/flowchart <description>` | Generate a flowchart diagram |
| `/sequence <description>` | Generate a sequence diagram |
| `/architecture <description>` | Generate an architecture diagram |
| `/mindmap <description>` | Generate a mindmap |
| `/flow <description>` | Alias for flowchart |
| `/diagram <description>` | Generic diagram (auto-detects type) |
| `/export <fmt> <description>` | Export diagram to file (png, svg, pdf, html, md) |
| `/delegate <agent> <task>` | Send task to any agent in the mesh |
| `/shared read [key]` | Read from shared memory |
| `/shared write key:value` | Write to shared memory |
| `/stats` | Agent statistics |

## Quick Start

/flowchart user login process
/sequence API request flow
/architecture microservices deployment
/mindmap project planning
/export html user login process

text

## Constitutional Status: 9/10 (FUNCTIONALLY CONSTITUTIONAL)

### What passes (8/8 core tests):
- ✅ 23-system boundary — lifecycle, enforcement, guarded executor, chronicle, metrics, security, etc.
- ✅ Capability routing — unrecognized commands auto-route to the correct agent
- ✅ Shared memory bridge — all diagrams and results persist to UnifiedMemory
- ✅ Cross-agent delegation — `/delegate` route + capability registry
- ✅ Exception logging — all errors logged via `log_err()`
- ✅ Interaction tracking — `track_interaction()` on every command
- ✅ Context gathering — WebClaw + DataClaw + Chronicle enrichment
- ✅ Circuit breaker — inherited from `BaseAgent.call_agent()`

### What's different (not a compliance gap):
- ⚠️ Sovereign Gateway — FlowClaw uses `self.llm` (LLMAdapter wrapping the DiagramEngine)
  instead of `self.ask_llm()`. This IS Article I compliant — all LLM access still routes
  through the Sovereign Gateway, just through a specialized diagram-generation adapter
  rather than the generic prompt method. The audit pattern doesn't detect this path.

## Architecture

FlowClaw uses a specialized LLM path because diagram generation requires:
1. Mermaid.js syntax validation
2. Diagram type detection (flowchart vs sequence vs architecture vs mindmap)
3. Browser-based rendering with syntax error recovery
4. Multi-format export (PNG, SVG, PDF, HTML, Markdown)

The `LLMAdapter` wraps the BaseAgent's Sovereign Gateway access with diagram-specific
prompt engineering and output validation. This is constitutional — Article I requires
all LLM access through the Sovereign Gateway, which FlowClaw does via `self.llm.call()`.

## Cross-Agent Integration

FlowClaw delegates to:
- **WebClaw** — search for diagram examples and documentation
- **DataClaw** — search local reference files
- **FileClaw** — export diagrams to files
- **Any agent** — via capability registry for unrecognized commands

Other agents call FlowClaw via:
- Capability registry: `/flow`, `/flowchart`, `/diagram`, `/mindmap`
- Direct delegation: `call_agent("flowclaw", "/flowchart login process")`

## Engine

- `engine/diagram_engine.py` — LLM-powered diagram generation with Mermaid syntax
- `engine/mermaid_validator.py` — Mermaid.js syntax validation
- `viewer/diagram_viewer.py` — Browser-based diagram rendering
- `exporters/base_exporter.py` — Multi-format export (DocxExporter, PdfExporter, HtmlExporter, MarkdownExporter, JsonExporter)
