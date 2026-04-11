# Chronicle Ledger System - Attribution

This chronicle/ledger system is inspired by and adapted from:

## Common_Chronicle
**Creator:** Liu Juanjuan (@liujuanjuan1984)
**Repository:** https://github.com/Intelligent-Internet/Common_Chronicle
**License:** Apache 2.0

### Original Concept
Common_Chronicle "turns messy context into structured, sourced timelines"

### Key Ideas Adapted
1. **Immutable ledger cards** - Every URL fetch creates a permanent record
2. **Context preservation** - Store surrounding text, source, timestamp
3. **Recovery by context** - Find URLs by what was said about them
4. **Timeline reconstruction** - Chronological view of discoveries
5. **Source attribution** - Know where each URL came from

### Integration into Clawpack
This implementation brings Common_Chronicle's chronicle/ledger pattern to Clawpack's webclaw agent, enabling:
- Full traceability of web searches
- Context-based URL recovery
- Audit trails for all fetched content

### License Compatibility
Apache 2.0 - Same as Common_Chronicle. This implementation remains
compatible with the original project's licensing terms.

---

*With thanks to Liu Juanjuan and the Common_Chronicle contributors for their innovative work on structured context management.*
