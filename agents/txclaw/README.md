# TXClaw — TX.org Blockchain Agent

**Exclusive AI agent for the TX.org blockchain ecosystem.**
Part of the Clawpack V2 21-agent runtime.

## Architecture

TXClaw queries two knowledge layers:
- **DataClaw** — 529 local documentation files across 17 domains (protobuf specs, API docs, service definitions)
- **WebClaw** — 135 verified live documentation URLs across 10 domains (docs.tx.org)

No file preloading. No hardcoded paths. Clean A2A delegation.

## Commands

| Command | Description |
|---------|-------------|
| `/tx <hash>` | Analyze transaction |
| `/block <height>` | Get block details |
| `/address <addr>` | Analyze address |
| `/token <symbol>` | Token information |
| `/validator <name>` | Validator details |
| `/contract <addr>` | Smart contract analysis |
| `/staking` | Staking overview |
| `/gas` | Gas fee structure |
| `/ecosystem` | Ecosystem overview |
| `/governance` | Governance proposals |
| `/network` | Network statistics |
| `/mempool` | Mempool status |
| `/generate <name>` | Generate CosmWasm contract |
| `/deploy <name>` | Deploy contract instructions |
| `/test <name>` | Generate unit tests |
| `/search <query>` | Search TX.org references |
| `/networks` | List network endpoints |
| `/stats` | Agent statistics |

## Reference Layers

### WebClaw (Online)
10 domains, 135 verified URLs at docs.tx.org:
api, dex, ecosystem, help, introduction, modules, nodes, security, services, tutorials

### DataClaw (Local)
17 domains, 529 files of offline documentation:
api, architecture, assets, blockchain, development, dex, ecosystem, governance,
ibc, introduction, modules, nodes, regulatory, security, services, smart_contracts, tutorials

## Part of Clawpack V2

21-agent local-first AI runtime with A2A routing on port 8766.
Constitutional governance. BM25 retrieval with source confidence scoring.
