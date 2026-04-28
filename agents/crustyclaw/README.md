# CrustyClaw

Pure Rust AI assistant with A2A routing, compiler validation, and standalone binary bridge.

## Features

- **Rust Code Generation** with `rustc` compiler validation
- **Cargo Integration** — run build, check, test, fmt, clippy from A2A
- **Standalone Binary Bridge** — uses crustyclaw binary for audit/pinch when available
- **Security Audit** — checks unsafe blocks, unwraps, dependencies
- **Pinch Mode** — detects unnecessary `.clone()` calls
- **A2A Routing** — integrates with WebClaw, TXClaw, LLMClaw

## Commands

| Command | Description |
|---------|-------------|
| `/rust <task>` | Generate Rust code with validation |
| `/code <task>` | Same as /rust |
| `/explain <concept>` | Explain Rust concepts |
| `/cargo <cmd>` | Run cargo (build, check, test, fmt, clippy) |
| `/audit <code>` | Security audit |
| `/pinch <path>` | Detect unnecessary clones |
| `/fix <code>` | Debug and fix |
| `/test <code>` | Generate unit tests |
| `/run` | cargo run |
| `/help` | Show help |
| `/stats` | Show statistics |

## Standalone Binary

CrustyClaw also exists as a standalone Rust binary at [greg-gzillion/crustyclaw](https://github.com/greg-gzillion/crustyclaw) with these features:

- `ask` — AI Q&A about your code
- `pinch` — Clone detection and optimization
- `audit` — Security auditing
- `shell` — Interactive lobster-themed terminal
- `status` — System status
- `prices` — Metal prices (PhoenixPME)
- `claw` — Display the lobster
- `molt` — Self-upgrade

The A2A agent automatically bridges to the standalone binary when available.

## File Structure
agents/crustyclaw/
├── agent_handler.py # A2A handler
├── commands/
│ ├── rust.py # Rust code generation
│ ├── explain.py # Concept explanation
│ └── cargo.py # Cargo operations
├── core/ # Core engine
├── src/ # Standalone Rust binary source
├── Cargo.toml # Rust dependencies
└── chronicle_bridge.py # Chronicle integration